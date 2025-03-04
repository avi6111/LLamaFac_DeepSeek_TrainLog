import torch
print("Check Cuda avaelabl.....")

if torch.cuda.is_available():
    print('Current Device index:',torch.cuda.current_device)
    print('Devce Name;',torch.cuda.get_device_name)
    print('D version:',torch.version.cuda)

    print('Cuda version:',torch.__version__)
else:
    print("Pytorch version:",torch.__version__)
    print('No Cuda Enviourment (可能是用的CPU）try:',torch.version.cuda)