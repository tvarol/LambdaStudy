import ROOT, sys, collections, math

def calXsec():
    xSec0 = (1 + (0.1*pow(float(kl),2)) - (99*float(kl)*(1./90.)))*30.56
    xSec1 = ((100*float(kl) - 10*pow(float(kl),2))*(1./90.))*14.42 
    xSec10 =((pow(float(kl),2) - float(kl))*(1./90.))*251.5
    xSec = xSec0 + xSec1 + xSec10
    return xSec

kl = sys.argv[1]

xsecVal = {'-10':659.7, '-6':306.1, '-4':180.2, '-2':88.33, '-1':55.22, '0':30.56, '1':14.42, '2':6.758, '4':16.96, '6':61.17, '10':251.5}
addedPoints = [2.2, 2.4, 2.6, 2.8, 3, 3.5, 5, 7, 8, 9, 15, 20, 25, -5, -7, -8, -9, -15, -20, -25]

if float(kl)>1:
    if (float(kl)*10)%10==0:
    	checkFileName = "hist-SM%sp.root"%(kl)
    else:
    	checkFileName = "hist-SM%sp.root"%(float(kl))
elif float(kl)<0:
    if (float(kl)*10)%10==0:
        checkFileName = "hist-SM%sm.root"%(abs(int(kl)))
    else:
        checkFileName = "hist-SM%sm.root"%(abs(float(kl)))
elif float(kl)==0:
    checkFileName = "hist-SM0.root"
elif float(kl)==1:
    checkFileName = "hist-SM.root"
print checkFileName


f = ROOT.TFile.Open(checkFileName)

histList=collections.OrderedDict()

histList=['mass_bbyy_1t_l', 'mass_bbyy_2t_l']

BR = 2*0.5824*0.00227

outputAccEff = file('accEff.csv','a')
outputYield = file('yield.csv','a')
outputXsec = file('xsec.csv','a')
outputAccEff.write('%s,'%(kl))
outputYield.write('%s,'%(kl))
outputXsec.write('%s,'%(kl))

for hist in histList:
     print hist 
     h = f.Get(hist)
     err = ROOT.Double()
     num = h.IntegralAndError(0,-1,err)
     if float(kl) in addedPoints:  
         denom = calXsec()*36.1*BR*(8.8111E-05/(1.4412E-02*7.8752E-03*0.34))
     else:
         denom = xsecVal[kl]*36.1*BR*(8.8111E-05/(1.4412E-02*7.8752E-03*0.34))
     print('numBefore = {}'.format(num))
     print('errBefore = {}'.format(err))
 
     if 100*err/num > 2:
         err = num*(2./100.)
     
     print('numAfter = {}'.format(num))
     print('errAfter = {}'.format(err))     
     outputAccEff.write(('%.4f,%.4f,'%(num/denom,err/denom)))
     outputYield.write(('%.4f,%.4f,'%(num,err)))
     outputXsec.write(('%.4f'%(denom)))
outputAccEff.write('\n')
outputAccEff.close()
outputYield.write('\n')
outputYield.close()
outputXsec.write('\n')
outputXsec.close()
