import mfr.modelSoln as m
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="parameter settings")
parser.add_argument("--nV",type=int,default=30)
parser.add_argument("--nVtilde",type=int,default=0)
parser.add_argument("--V_bar",type=float,default=1.0)
parser.add_argument("--Vtilde_bar",type=float,default=0.0)
parser.add_argument("--sigma_V_norm",type=float,default=0.132)
parser.add_argument("--sigma_Vtilde_norm",type=float,default=0.0)

parser.add_argument("--a_e",type=float,default=0.14)
parser.add_argument("--a_h",type=float,default=0.135)
parser.add_argument("--psi_e",type=float,default=1.0)
parser.add_argument("--psi_h",type=float,default=1.0)
parser.add_argument("--gamma_e",type=float,default=1.0)
parser.add_argument("--gamma_h",type=float,default=1.0)
parser.add_argument("--chiUnderline",type=float,default=1.0)
args = parser.parse_args()

params = m.paramsDefault.copy()

## Dimensionality params
params['nDims']             = 3
params['nShocks']           = 3

## Grid parameters 
params['numSds']            = 5
params['uselogW']           = 0

params['nWealth']           = 100
params['nZ']                = 30
params['nV']                = args.nV
params['nVtilde']           = args.nVtilde


## Economic params
params['nu_newborn']        = 0.1
params['lambda_d']          = 0.02
params['lambda_Z']          = 0.252
params['lambda_V']          = 0.156
params['lambda_Vtilde']     = 1.38
params['delta_e']           = 0.05
params['delta_h']           = 0.05
params['a_e']               = args.a_e
params['a_h']               = args.a_h
params['rho_e']             = args.psi_e
params['rho_h']             = args.psi_h
params['phi']               = 3.0
params['gamma_e']           = args.gamma_e
params['gamma_h']           = args.gamma_h
params['equityIss']         = 2
params['chiUnderline']      = args.chiUnderline
params['alpha_K']           = 0.05

## Alogirthm behavior and results savings params
params['method']            = 2
params['dt']                = 0.1
params['dtInner']           = 0.1

params['tol']               = 1e-5
params['innerTol']          = 1e-5

params['verbatim']          = -1
params['maxIters']          = 4000
params['maxItersInner']     = 2000000
params['iparm_2']           = 28
params['iparm_3']           = 0
params['iparm_28']          = 0
params['iparm_31']          = 0
params['overwrite']         = 'Yes'
params['exportFreq']        = 10000
params['CGscale']           = 1.0
params['hhCap']             = 1
params['preLoad']           = 'None'

# Domain params
params['Vtilde_bar']        = args.Vtilde_bar
params['Z_bar']             = 0.0
params['V_bar']             = args.V_bar
params['sigma_K_norm']      = 0.01
params['sigma_Z_norm']      = 0.0141
params['sigma_V_norm']      = args.sigma_V_norm
params['sigma_Vtilde_norm'] = args.sigma_Vtilde_norm
params['wMin']              = 0.01
params['wMax']              = 0.99

## Shock correlation params
params['cov11']             = 1.0
params['cov12']             = 0.0
params['cov13']             = 0.0
params['cov14']             = 0.0
params['cov21']             = 0.0
params['cov22']             = 1.0
params['cov23']             = 0.0
params['cov24']             = 0.0
params['cov31']             = 0.0
params['cov32']             = 0.0
params['cov33']             = 1.0
params['cov34']             = 0.0
params['cov41']             = 0.0
params['cov42']             = 0.0
params['cov43']             = 0.0
params['cov44']             = 0.0

psi_e = str("{:0.3f}".format(params['rho_e'])).replace('.', '', 1) 
psi_h = str("{:0.3f}".format(params['rho_h'])).replace('.', '', 1) 
gamma_e = str("{:0.3f}".format(params['gamma_e'])).replace('.', '', 1) 
gamma_h = str("{:0.3f}".format(params['gamma_h'])).replace('.', '', 1) 
a_e = str("{:0.3f}".format(params['a_e'])).replace('.', '', 1) 
a_h = str("{:0.3f}".format(params['a_h'])).replace('.', '', 1) 
chiUnderline = str("{:0.3f}".format(params['chiUnderline'])).replace('.', '', 1) 

folder_name = 'chiUnderline_' + chiUnderline + '_a_e_' + a_e + '_a_h_' + a_h  + '_gamma_e_' + gamma_e + '_gamma_h_' + gamma_h + '_psi_e_' + psi_e + '_psi_h_' + psi_h

params['folderName']        = folder_name

#### Now, create a Model
testModel = m.Model(params)

# Step 2: Solve the model
#------------------------------------------#

#### This step is very simple: use the .solve() method.
testModel.solve()
testModel.printInfo() ## This step is optional: it prints out information regarding time, number of iterations, etc.
testModel.printParams() ## This step is optional: it prints out the parameteres used.


testModel.dumpData()


# %%



### Step 3: Compute stationary density
##------------------------------------------#

##### This method can only be called after the model is solved.
testModel.computeStatDent()

### Step 4: Compute moments and correlation
##------------------------------------------#

##### This step can only be completed after computing the stationary dneisty.
# testModel.computeMoments(['W', 'r'])

##### In this example, we want to see the mean and standard deviation of
##### the wealth share and interest rate. The input is a list of the variables
##### that you would like to compute moments for. The nomenclature is such that
##### the method minus "()". For example, you would access variable r through
##### testModel.r(). To configure the inputs for this function, ignore "()".

##### After computing moments, you can access them through testModel.moments,
##### where the first moment is the mean and second is sd.
# print(testModel.macroMoments)
# print(testModel.apMoments)

##### You can access the FK matrix used to compute for the stationary density
##### by testModel.FKmat

##### To compute correlations, the procedure is very similar. To access
##### the correlations, call testModel.corrs.
# testModel.computeCorrs(['W', 'r'])
# print(testModel.corrs)

### Step 5: Compute shock elasticities
##------------------------------------------#

##### To compute shock elsaticities, we recommend that you compute stationary density
##### beforehand, so that we can select quintiles from the distribution.

##### Method 1:
#####  You may put in the quintiles of the state variable in a dictionary and use
#####  it as the input for argument pcts (as shown below). Other arguments needed
#####  include T, dt, and perturb, where perturb is the variable you want to shock.
#####  If you'd like to shock consumption, put in "C" as you would normally use
#####  testModel.C() to get consumption. By default, if we use zero first derivatives
#####  as the boundary conditions. For a more detailed discussion, refer to documentation
#####  on mfr.sem.

# testModel.computeShockElas(pcts = {'W':[.3,.7], 'Z': [0.3, 0.7], 'V': [0.3, 0.7]}, T = 100, dt = 1, perturb = 'C')

##### Method 2:
#####  You may also put in the actual values of the starting points. All other
#####  arguments are the same

# testModel.computeShockElas(points = np.matrix('0.2, 0.0, 1.0; 0.5, 0.0, 1.5') , T = 100, dt = 1, perturb = 'C')

##### Access
#####  To access the shock elasticities, you can use the following three attributes.
#####  Note that the output is the same as described in the documentation for mfr.sem.
#####    testModel.expoElas  (exposure elasticities)
#####    testModel.priceElasHouseholds (price elasticities using households sdf)
#####    testModel.priceElasExperts  (price elasticities using experts sdf)
#####  Furthermore, you can access the linear systems through
#####    testModel.linSysExpo (linear system used to solve for the exposure elasticities)
#####    testModel.linSysH   (linear system used to solve for households' elasticities)
#####    testModel.linSysE   (linear system used to solve for experts' elasticities)
