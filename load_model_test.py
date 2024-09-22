import torch

surf_cond_id = 2
wthr_cond_id = 3
light_cond_id = 4

data = '18039324,1/1/2021 10:50,65,3,'+ str(surf_cond_id) + ',' + str(wthr_cond_id) + ',' + str(light_cond_id) + ',' + '1,,0,0,5,0,2,IH 10 W,410,2,2\n'


# Predict Risk using pretrained AI model with a SINGLE sample (example seems to be in Sahidul's evaluate() function)
device = 'cpu'
# load pretrained model
net = torch.load('Safety_net_0.pkl')
print(net)
net = net.float().to(device) # tells pytorch whether to use CPU or GPU. Use CPU
# put model in eval mode (there are different modes: train, eval (test model), etc...)
net.eval()
#input_data = torch.rand(1,1,62,1)
input_data = torch.tensor([[[[16559000.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [0.0], [30.0], [0.0], [0.0], [11.0], [4.0], [0.0], [1.0], [1.0], [20.0], [254.0], [27.544], [-99.511], [1.0], [0.0], [0.0], [8.0], [1.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0]]]])
#print(input_data)
# pass input data into model and receive output prediction(s)
outputs_test = net(input_data) # input data should be a TENSOR of shape: (#samples x 1 x 62 features x 1)
print("Output: ", outputs_test)

_, predicted_test = torch.max(outputs_test.data, 1)

# The output is between 0 to 5, representing unknown, serious, minor, possible, fatal, no-injury. 
print("Predicted: ", predicted_test)
