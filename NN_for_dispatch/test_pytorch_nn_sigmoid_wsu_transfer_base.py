#pytorch tests
import numpy as np 
import xlrd
import torch

def train_nn_sigmoid(layers=4):
    dtype = torch.float
    #device = torch.device("cpu")
    device = torch.device("cuda:0")


    load_e = []
    load_h = []
    load_c = []
    t_db = []
    irrad = []

    wb = xlrd.open_workbook('c:/Users/Nadia Panossian/Documents/GitHub/EAGERS_wsu/GUI/Optimization/Results/wsu_campus_2009_2012.xlsx')
    sheet = wb.sheet_by_index(0)
    n_disps = 365*24
    inputs= torch.zeros(n_disps,16)#, device=device, dtype=dtype)
    e_dem_max = [3787.993,6311.181,4533.527,378.7993]#sheet.cell_value(1,7)
    h_dem_max = [7570.097,12612.55,9060.006,757.0097]#sheet.cell_value(1,8)
    c_dem_max = [8345.065,13903.73,9987.5,834.5065]#sheet.cell_value(1,9)
    cost_max = 0.07#sheet.cell_value(1,12)
    for row in range(1,n_disps):
        inputs[row-1,0] = sheet.cell_value(row,0)*38480/117415.7/e_dem_max[2]#E_dem_0
        inputs[row-1,1] = sheet.cell_value(row,0)*38480/117415.7/e_dem_max[2]#E_dem_1
        inputs[row-1,2] = sheet.cell_value(row,0)*32152/117415.7/e_dem_max[0]#E_dem_2
        inputs[row-1,3] = sheet.cell_value(row,0)*53568.5/117415.7/e_dem_max[1]#E_dem_3
        inputs[row-1,4] = sheet.cell_value(row,0)*3215.2/117415.7/e_dem_max[3]#E_dem_4
        inputs[row-1,5] = sheet.cell_value(row,0)*38480/117415.7/e_dem_max[2]#E_dem_5
        inputs[row-1,6] = sheet.cell_value(row,0)*3215.2/117415.7/e_dem_max[3]#E_dem_6
        inputs[row-1,7] = sheet.cell_value(row,1)*32152/117415.7/h_dem_max[0]#H_dem_2
        inputs[row-1,8] = sheet.cell_value(row,1)*53568.5/117415.7/h_dem_max[1]#H_dem_3
        inputs[row-1,9] = sheet.cell_value(row,1)*38480/117415.7/h_dem_max[2]#H_dem_4
        inputs[row-1,10] = sheet.cell_value(row,1)*3215.2/117415.7/h_dem_max[3]#H_dem_5
        inputs[row-1,11] = sheet.cell_value(row,2)*32152/117415.7/c_dem_max[0]#C_dem_2
        inputs[row-1,12] = sheet.cell_value(row,2)*53568.5/117415.7/c_dem_max[1]#C_dem_3
        inputs[row-1,13] = sheet.cell_value(row,2)*38480/117415.7/c_dem_max[2]#C_dem_4
        inputs[row-1,14] = sheet.cell_value(row,2)*3215.2/117415.7/c_dem_max[3]#C_dem_5
        inputs[row-1,15] = 1#sheet.cell_value(row,4)/cost_max #utility electric cost
        # inputs[row-2,0] = sheet.cell_value(row,1)#E_dem
        # inputs[row-2,1] = sheet.cell_value(row,2)#H_dem
        # inputs[row-2,2] = sheet.cell_value(row,3)#C_dem
        # inputs[row-2,3] = sheet.cell_value(row,4)/cost_max #utility electric cost
        #inputs[row-2,3] = sheet.cell_value(row,4)/sheet.cell_value(1,10)#Temp_db_C
        #inputs[row-2,4] = sheet.cell_value(row,5)/sheet.cell_value(1,11)#Direct_normal_irradiance
        # load_e.append(row)
        # load_h.append(row[1])
        # load_c.append(row[2])
        # t_db.append(row[3])
        # irrad.append(row[4])
        # inputs.append(row)

    #inputs[:,1] = (inputs[:,1]-min(inputs[:,1]))/h_dem_max
    #inputs[:,2] = (inputs[:,2]-min(inputs[:,2]))/c_dem_max
    # inputs[:,1] = inputs[:,1]/h_dem_max
    # inputs[:,2] = inputs[:,2]/c_dem_max


    print('inputs read')

    wb = xlrd.open_workbook('c:/Users/Nadia Panossian/Documents/GitHub/EAGERS_wsu/GUI/Optimization/Results/wsu_cqp.xlsx')
    sheet = wb.sheet_by_index(0)
    disp = torch.zeros(n_disps,23)#, device=device, dtype=dtype)
    for row in range(1,n_disps):
        r = row-1
        # inputs[r,0] -=sheet.cell_value(row,1)
        disp[r,0] = sheet.cell_value(row,3)/2500#GT1
        disp[r,1] = sheet.cell_value(row,15)/2187.5#GT2
        disp[r,2] = sheet.cell_value(row,24)/1375#GT3
        disp[r,3] = sheet.cell_value(row,25)/1375#GT4
        disp[r,4] = sheet.cell_value(row,6)/20000#boiler1
        disp[r,5] = sheet.cell_value(row,17)/20000#boiler2
        disp[r,6] = sheet.cell_value(row,18)/20000#boiler3
        disp[r,7] = sheet.cell_value(row,19)/20000#boiler4
        disp[r,8] = sheet.cell_value(row,20)/20000#boiler5
        disp[r,9] = sheet.cell_value(row,4)/(7.279884675000000e+03)#carrier1
        disp[r,10] = sheet.cell_value(row,7)/(5.268245045000001e+03)#york1
        disp[r,11] = sheet.cell_value(row,8)/(5.268245045000001e+03)#york3
        disp[r,12] = sheet.cell_value(row,9)/(5.275278750000000e+03)#carrier7
        disp[r,13] = sheet.cell_value(row,10)/(5.275278750000000e+03)#carrier8
        disp[r,14] = sheet.cell_value(row,11)/(4.853256450000000e+03)#carrier2
        disp[r,15] = sheet.cell_value(row,12)/(4.853256450000000e+03)#carrier3
        disp[r,16] = sheet.cell_value(row,13)/(1.758426250000000e+03)#carrier4
        disp[r,17] = sheet.cell_value(row,14)/(1.415462794200000e+03)#trane
        disp[r,18] = sheet.cell_value(row,5)/2000000#cold water tank

        disp[r,19] = 0.05#.9/1.1#sheet.cell_value(row,11)#voltage0#GT1 reactive
        disp[r,20] = 0.05#1.1/1.1#sheet.cell_value(row,12)#voltage1# GT2 reactive
        disp[r,21] = 0.05#.9/1.1#sheet.cell_value(row,13)#voltage2# GT3 reactive
        disp[r,22] = 0.05#.9/1.1#sheet.cell_value(row,13)#voltage3# GT4 reactive
        #disp[r,23] = .9/1.1#sheet.cell_value(row,14)#voltage4
        #disp[r,24] = .9/1.1#sheet.cell_value(row,15)#voltage5
        #disp[r,25] = .9/1.1#voltage6
        # disp[r,0] = sheet.cell_value(row,2)/7000#GT1
        # disp[r,1] = sheet.cell_value(row,3)/5000#GT2
        # disp[r,2] = sheet.cell_value(row,4)/2000#FC1
        # disp[r,3] = sheet.cell_value(row,5)/2000#FC2
        # disp[r,4] = sheet.cell_value(row,6)/500#sGT
        # disp[r,5] = sheet.cell_value(row,7)/1500#Diesel
        # disp[r,6] = sheet.cell_value(row,8)/20000#Heater
        # disp[r,7] = sheet.cell_value(row,9)/10000#chiller1
        # disp[r,8] = sheet.cell_value(row,10)/10000#chiller2
        # disp[r,9] = sheet.cell_value(row,11)/7500#small Chiller1
        # disp[r,10] = sheet.cell_value(row,12)/7500#small Chiller2
        # disp[r,11] = sheet.cell_value(row,13)/30000#battery
        # disp[r,12] = sheet.cell_value(row,14)/75000#hot water tank
        # disp[r,13] = sheet.cell_value(row,15)/200000#cold water tank
        renew_gen = sheet.cell_value(row+1, 21) + sheet.cell_value(row+1,22)#sheet.cell_value(row+1,12) #solar generation
        inputs[row-2,6] = inputs[row-2,6]-max(renew_gen,0)/e_dem_max[3]

    # inputs[:,0] = inputs[:,0]/e_dem_max#inputs[:,0] = (inputs[:,0]-min(inputs[:,0]))/max(inputs[:,0])
    #inputs[1:,4:] = disp[:-1,:]
    inputs = inputs[1:,:]
    disp = disp[1:,:]
    print('outputs read')

    #shuffle and separate training from testing
    shuffled = [inputs,disp]
    shuffled = torch.randperm(len(inputs[:,0]))
    split_line = int(np.floor(len(inputs[:,0])/10))
    inputs = inputs[shuffled,:]
    disp = disp[shuffled,:]
    inputs_train = inputs[:-split_line,:]
    inputs_test = inputs[-split_line:, :]
    disp_train = disp[:-split_line, :]
    disp_test = disp[-split_line:, :]
    disp = disp_train
    inputs = inputs_train


    #batch size, input dimension hidden dimension, output dimension
    N, D_in, H, D_out = len(inputs[:,0]), len(inputs[0,:]), int(np.ceil(len(inputs[0,:])+len(disp[0,:])/2)), len(disp[0,:])
    H2 = int(np.round(H*1.2))
    H3 = int(np.round(H*0.8))
    H4 = H2

    x = inputs
    y = disp

    if layers == 1:
        model = torch.nn.Sequential(
            torch.nn.Sigmoid(D_in, D_out)
        )
    elif layers == 2:
        model = torch.nn.Sequential(
        torch.nn.Sigmoid(),
        torch.nn.ReLU(),
        torch.nn.Linear(D_in, D_out) 
        )
    elif layers == 3:
        model = torch.nn.Sequential(
        torch.nn.Sigmoid(),
        torch.nn.ReLU(),
        torch.nn.Linear(D_in, H),
        torch.nn.ReLU(),
        torch.nn.Linear(H, D_out)
        )
    elif layers == 4:
        model = torch.nn.Sequential(
        torch.nn.Sigmoid(),
        torch.nn.ReLU(),
        torch.nn.Linear(D_in, H),
        torch.nn.ReLU(),
        torch.nn.Linear(H, H),
        torch.nn.ReLU(),
        torch.nn.Linear(H, D_out)
        )
    elif layers == 5:
        model = torch.nn.Sequential(
        torch.nn.Sigmoid(),
        torch.nn.ReLU(),
        torch.nn.Linear(D_in, H),
        torch.nn.ReLU(),
        torch.nn.Linear(H, H2),
        torch.nn.ReLU(),
        torch.nn.Linear(H2, H),
        torch.nn.ReLU(),
        torch.nn.Linear(H, D_out)
        )
    elif layers == 6:
        model = torch.nn.Sequential(
        torch.nn.Sigmoid(),
        torch.nn.ReLU(),
        torch.nn.Linear(D_in, H),
        torch.nn.ReLU(),
        torch.nn.Linear(H, H2),
        torch.nn.ReLU(),
        torch.nn.Linear(H2, H3),
        torch.nn.ReLU(),
        torch.nn.Linear(H3, H),
        torch.nn.ReLU(),
        torch.nn.Linear(H, D_out)
        )
    else: #layers = 7
        model = torch.nn.Sequential(
            torch.nn.Sigmoid(),
            torch.nn.ReLU(),
            torch.nn.Linear(D_in, H),
            torch.nn.ReLU(),
            torch.nn.Linear(H, H2),
            torch.nn.ReLU(),
            torch.nn.Linear(H2, H3),
            torch.nn.ReLU(),
            torch.nn.Linear(H3, H2),
            torch.nn.ReLU(),
            torch.nn.Linear(H2, H),
            torch.nn.ReLU(),
            torch.nn.Linear(H, D_out)
        )


    loss_fn = torch.nn.MSELoss(reduction='sum')
    n_iters = 50000
    loss_rate = np.zeros(n_iters)

    learning_rate = 1e-6
    for t in range(n_iters):
        y_pred = model(x)

        loss = loss_fn(y_pred, y)
        print(t, loss.item())
        loss_rate[t] = loss.item()

        model.zero_grad()

        loss.backward()

        with torch.no_grad():
            for param in model.parameters():
                param -= learning_rate *param.grad

    y_pred_np = y_pred.detach().numpy()
    y_np = y.detach().numpy()
    acc = sum((y_pred_np-y_np)**2)/len(y[:,0])
    #a = 0

    #test
    y_pred = model(inputs_test)
    y_pred_test = y_pred.detach().numpy()
    y_test = disp_test.detach().numpy()
    acc_test = sum((y_pred_test-y_test)**2)/len(y_test[:,0])
    #b=0

    # input_scale_factors = np.array([e_dem_max, h_dem_max, c_dem_max, cost_max])
    # output_scale_factors = np.array([7000, 5000, 2000, 2000, 500, 1500, 20000, 10000, 10000, 7500, 7500, 30000, 75000, 200000])
    input_scale_factors = np.array([e_dem_max[2], e_dem_max[2], e_dem_max[0], e_dem_max[1], e_dem_max[3], e_dem_max[2], e_dem_max[3],\
        h_dem_max[0], h_dem_max[1], h_dem_max[2], h_dem_max[3], c_dem_max[0], c_dem_max[1], c_dem_max[2], c_dem_max[3], cost_max])
    output_scale_factors = np.array([2500, 2187.5, 1375, 1375, 20000, 20000, 20000, 20000, 20000,\
        7.279884675000000e+03, 5.268245045000001e+03, 5.268245045000001e+03, 5.275278750000000e+03, 5.275278750000000e+03, 4.853256450000000e+03,\
        4.853256450000000e+03, 1.758426250000000e+03, 1.758426250000000e+03, 2000000, 2500, 2187.5, 1375, 1375])

    print('nn trained, beginning transfer learning')
    ##################### next train on the conic solutions
    wb = xlrd.open_workbook('c:/Users/Nadia Panossian/Documents/GitHub/EAGERS_wsu/GUI/Optimization/Results/conic_analysis_01.xlsx')
    sheet = wb.sheet_by_index(1)
    n_disps = int(round(100))
    inputs= torch.zeros(n_disps,16)#, device=device, dtype=dtype)
    e_dem_max = [3787.993,6311.181,4533.527,378.7993]#sheet.cell_value(1,7)
    h_dem_max = [7570.097,12612.55,9060.006,757.0097]#sheet.cell_value(1,8)
    c_dem_max = [8345.065,13903.73,9987.5,834.5065]#sheet.cell_value(1,9)
    cost_max = 0.07#sheet.cell_value(1,12)
    for row in range(n_disps):
        r = (row*24)+1
        inputs[row,0] = sheet.cell_value(r,111)*38480/117415.7/e_dem_max[2]#E_dem_0
        inputs[row,1] = sheet.cell_value(r,111)*38480/117415.7/e_dem_max[2]#E_dem_1
        inputs[row,2] = sheet.cell_value(r,111)*32152/117415.7/e_dem_max[0]#E_dem_2
        inputs[row,3] = sheet.cell_value(r,111)*53568.5/117415.7/e_dem_max[1]#E_dem_3
        inputs[row,4] = sheet.cell_value(r,111)*3215.2/117415.7/e_dem_max[3]#E_dem_4
        inputs[row,5] = sheet.cell_value(r,111)*38480/117415.7/e_dem_max[2]#E_dem_5
        inputs[row,6] = (sheet.cell_value(r,111)-sheet.cell_value(r,110))*3215.2/117415.7/e_dem_max[3]#E_dem_6
        inputs[row,7] = sheet.cell_value(r,112)*32152/117415.7/h_dem_max[0]#H_dem_2
        inputs[row,8] = sheet.cell_value(r,112)*53568.5/117415.7/h_dem_max[1]#H_dem_3
        inputs[row,9] = sheet.cell_value(r,112)*38480/117415.7/h_dem_max[2]#H_dem_4
        inputs[row,10] = sheet.cell_value(r,112)*3215.2/117415.7/h_dem_max[3]#H_dem_5
        inputs[row,11] = sheet.cell_value(r,113)*32152/117415.7/c_dem_max[0]#C_dem_2
        inputs[row,12] = sheet.cell_value(r,113)*53568.5/117415.7/c_dem_max[1]#C_dem_3
        inputs[row,13] = sheet.cell_value(r,113)*38480/117415.7/c_dem_max[2]#C_dem_4
        inputs[row,14] = sheet.cell_value(r,113)*3215.2/117415.7/c_dem_max[3]#C_dem_5
        inputs[row,15] = 1#sheet.cell_value(r,116)/cost_max #utility electric cost

    print('conic inputs read')

    wb = xlrd.open_workbook('c:/Users/Nadia Panossian/Documents/GitHub/EAGERS_wsu/GUI/Optimization/Results/conic_analysis_mod3.xlsx')
    sheet = wb.sheet_by_index(1)
    disp = torch.zeros(n_disps,23)#, device=device, dtype=dtype)
    for r in range(n_disps):
        row = r*24+1
        # inputs[r,0] -=sheet.cell_value(row,1)
        disp[r,0] = sheet.cell_value(row,40)/2500#GT1
        disp[r,1] = sheet.cell_value(row,41)/2187.5#GT2
        disp[r,2] = sheet.cell_value(row,42)/1375#GT3
        disp[r,3] = sheet.cell_value(row,43)/1375#GT4
        disp[r,4] = sheet.cell_value(row,57)/20000#boiler1
        disp[r,5] = sheet.cell_value(row,58)/20000#boiler2
        disp[r,6] = sheet.cell_value(row,59)/20000#boiler3
        disp[r,7] = sheet.cell_value(row,60)/20000#boiler4
        disp[r,8] = sheet.cell_value(row,61)/20000#boiler5
        disp[r,9] = sheet.cell_value(row,67)/(7.279884675000000e+03)#carrier1
        disp[r,10] = sheet.cell_value(row,68)/(5.268245045000001e+03)#york1
        disp[r,11] = sheet.cell_value(row,69)/(5.268245045000001e+03)#york3
        disp[r,12] = sheet.cell_value(row,70)/(5.275278750000000e+03)#carrier7
        disp[r,13] = sheet.cell_value(row,71)/(5.275278750000000e+03)#carrier8
        disp[r,14] = sheet.cell_value(row,72)/(4.853256450000000e+03)#carrier2
        disp[r,15] = sheet.cell_value(row,73)/(4.853256450000000e+03)#carrier3
        disp[r,16] = sheet.cell_value(row,74)/(1.758426250000000e+03)#carrier4
        disp[r,17] = sheet.cell_value(row,75)/(1.415462794200000e+03)#trane
        disp[r,18] = sheet.cell_value(row,96)/2000000#cold water tank

        disp[r,0] = sheet.cell_value(row,44)/2500#GT1 reactive
        disp[r,1] = sheet.cell_value(row,45)/2187.5#GT2 reactive
        disp[r,2] = sheet.cell_value(row,46)/1375#GT3 reactive
        disp[r,3] = sheet.cell_value(row,47)/1375#GT4 reactive


    #shuffle and separate training from testing
    shuffled = [inputs,disp]
    shuffled = torch.randperm(len(inputs[:,0]))
    split_line = int(np.floor(len(inputs[:,0])/10))
    inputs = inputs[shuffled,:]
    disp = disp[shuffled,:]
    inputs_train = inputs[:-split_line,:]
    inputs_test = inputs[-split_line:, :]
    disp_train = disp[:-split_line, :]
    disp_test = disp[-split_line:, :]
    disp = disp_train
    inputs = inputs_train
    y = disp
    x = inputs

    # transfer learned nn to conic problem
    n_iters = int(round(n_iters/10))
    for t in range(n_iters):
        y_pred = model(x)

        loss = loss_fn(y_pred, y)
        print(t, loss.item())
        loss_rate[t] = loss.item()

        model.zero_grad()

        loss.backward()

        with torch.no_grad():
            for param in model.parameters():
                param -= learning_rate *param.grad

    y_pred_np = y_pred.detach().numpy()
    y_np = y.detach().numpy()
    acc = sum((y_pred_np-y_np)**2)/len(y[:,0])

    #test
    y_pred = model(inputs_test)
    y_pred_test = y_pred.detach().numpy()
    y_test = disp_test.detach().numpy()
    acc_test = sum((y_pred_test-y_test)**2)/len(y_test[:,0])

    return model, acc, acc_test, input_scale_factors, output_scale_factors, loss_rate

def fire_nn(model, scaled_inputs):
    y_pred = model(scaled_inputs)
    return y_pred
    
