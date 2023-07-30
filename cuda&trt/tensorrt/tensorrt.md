# tensorrt

tensorrt可以使用API搭建网络，也可以使用onnx解析已有的权重自动搭建网络

## 1. pytorch转onnx

使用pytorch自带的onnx接口即可：

```python
torch.onnx.export(
    model, # 模型
    t.randn(1, 1, nHeight, nWidth, device="cuda"), # 输入数据的维度
    onnxFile, # 导出onnx的文件名
    input_names=["x"], # 输入的名称
    output_names=["y", "z"], # 输出的名称，此处输出有2
    do_constant_folding=True, # 常量折叠
    verbose=True, # 输出日志等级
    keep_initializers_as_inputs=True, # 保留模型的初始化参数作为输入
    opset_version=12, # 建议11及以上
    dynamic_axes={"x": {0: "nBatchSize"}, "z": {0: "nBatchSize"}} # 动态维度（BCHW）
)
```

## 2. onnx转plan

onnx文件转plan引擎文件有两种方式：

1. 通过python接口
2. 通过trtexec

### 2.1 python接口

```python
import tensorrt as trt
import os

bUseFP16Mode = True
onnxFile = "./model.onnx"
trtFile = "./modelfp16.plan"
nHeight = 540
nWidth = 960

logger = trt.Logger(trt.Logger.VERBOSE)
builder = trt.Builder(logger)
network = builder.create_network(
    1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
)
profile = builder.create_optimization_profile()
config = builder.create_builder_config()
if bUseFP16Mode:
    config.set_flag(trt.BuilderFlag.FP16)

parser = trt.OnnxParser(network, logger)
if not os.path.exists(onnxFile):
    print("Failed finding ONNX file!")
    exit()
print("Succeeded finding ONNX file!")
with open(onnxFile, "rb") as model:
    if not parser.parse(model.read()):
        print("Failed parsing .onnx file!")
        for error in range(parser.num_errors):
            print(parser.get_error(error))
        exit()
    print("Succeeded parsing .onnx file!")

inputTensor = network.get_input(0)
profile.set_shape(
    inputTensor.name,
    min=[1, 3, nHeight, nWidth], # 动态输入大小的最小值
    opt=[4, 3, nHeight, nWidth], # 最常见值
    max=[8, 3, nHeight, nWidth], # 最大值
)
config.add_optimization_profile(profile)

engineString = builder.build_serialized_network(network, config) # 序列化网络
if engineString == None:
    print("Failed building engine!")
    exit()
print("Succeeded building engine!")
with open(trtFile, "wb") as f:
    f.write(engineString)
```

### 2.2 trtexec

``` shell
trtexec --onnx=model.onnx --saveEngine=model.plan --fp16
```

## 3. 运行

```python
import tensorrt as trt
import os
import cv2
import numpy as np
from cuda import cudart

bUseFP16Mode = True
bUseINT8Mode = False
nHeight = 1080//2
nWidth = 1920//2
plan_name = "modelfp32.plan"

logger = trt.Logger(trt.Logger.VERBOSE)

with open(plan_name, 'rb') as f:
    engine = trt.Runtime(logger).deserialize_cuda_engine(f.read()) # 加载并反序列化plan文件
nIO = engine.num_io_tensors
lTensorName = [engine.get_tensor_name(i) for i in range(nIO)]
nInput = [engine.get_tensor_mode(lTensorName[i])
          for i in range(nIO)].count(trt.TensorIOMode.INPUT)

context = engine.create_execution_context()
context.set_input_shape(lTensorName[0], [1, 3, nHeight, nWidth])
for i in range(nIO):
    print("[%2d]%s->" % (i, "Input " if i < nInput else "Output"), engine.get_tensor_dtype(lTensorName[i]),
          engine.get_tensor_shape(lTensorName[i]), context.get_tensor_shape(lTensorName[i]), lTensorName[i])

bufferH = []
data = cv2.imread('2.jpg').astype(np.float32).reshape(1, 3, nHeight, nWidth)
data = data/255
print(data.shape)
bufferH.append(np.ascontiguousarray(data))
for i in range(nInput, nIO):
    bufferH.append(np.empty(context.get_tensor_shape(
        lTensorName[i]), dtype=trt.nptype(engine.get_tensor_dtype(lTensorName[i]))))
bufferD = []
for i in range(nIO):
    bufferD.append(cudart.cudaMalloc(bufferH[i].nbytes)[1])

for i in range(nInput):
    cudart.cudaMemcpy(bufferD[i], bufferH[i].ctypes.data,
                      bufferH[i].nbytes, cudart.cudaMemcpyKind.cudaMemcpyHostToDevice)

for i in range(nIO):
    context.set_tensor_address(lTensorName[i], int(bufferD[i]))
context.execute_async_v3(0)
for i in range(nInput, nIO):
    cudart.cudaMemcpy(bufferH[i].ctypes.data, bufferD[i],
                      bufferH[i].nbytes, cudart.cudaMemcpyKind.cudaMemcpyDeviceToHost)

for i in range(nIO):
    print(lTensorName[i])
    print(bufferH[i].shape)
    img = bufferH[i].reshape(bufferH[i].shape[2],bufferH[i].shape[3],3)
    img = np.round(img * 255.0).astype('uint8')
    cv2.imwrite('./3_fp32.jpg',img)

for b in bufferD:
    cudart.cudaFree(b)

print("Succeeded running model in TensorRT!")
```

