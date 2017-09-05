Setting up the environment
---------------------------

`setenv SCRAM_ARCH slc6_amd64_gcc481`  
`cmsrel CMSSW_7_1_5`  
`cd CMSSW_7_1_5/src`  
`cmsenv`  
`git clone  --branch v5.0.2 https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit`  
`mkdir CombinedEWKAnalysis`  
`git clone https://github.com/svefontana/CombinedEWKAnalysis_1D2D3D CombinedEWKAnalysis`  
`source CombinedEWKAnalysis/CommonTools/setup/patchToSource.sh`  
`scram b`  
`cd CombinedEWKAnalysis/CommonTools/test`  

To calculate 1D limits for fs1: 
-----------------------------

Change path to data file at the beginning of test_fs.py    
`python test_fs.py`  creates the signal input files ch_eee_fs, ch_eem_fs,ch_mme_fs,ch_mmm_fs which are needed as input for doFit_nonuniformbins_bin_separated.py  
`python doFit_nonuniformbins_bin_separated.py --config=config_WZ_fs`     
`python buildWorkspace_AC.py --config=config_WZ_fs_bkg` Needs the input files with data and background histograms and the corresponding uncertainties. Example input files are in CombinedEWKAnalysis/CommonTools/data/anomalousCoupling  eee_bin1.root - mmm_bin8.root.   
They are made with (This code needs the output of the DevTools framework as input):  
*python data_bkg_histos_bin_separated.py*     
*python correct_uncertaintybands.py*     
*python pdfweight_variation_bin_separated.py*      
*python scale_variation_bin_separated.py*  

`combineCards.py aC_eee_bin*.txt aC_eem_bin*.txt aC_mme_bin*.txt aC_mmm_bin*.txt > aC_WZ_all_fs.txt`  
`text2workspace.py -m 126 aC_WZ_all_fs.txt -o Example_WZ_fs.root -P CombinedEWKAnalysis.CommonTools.ACModel:par1_TF1_Model --PO channels=eee_bin1,eee_bin2,eee_bin3,eee_bin4,eee_bin5,eee_bin6,eee_bin7,eee_bin8,eem_bin1,eem_bin2,eem_bin3,eem_bin4,eem_bin5,eem_bin6,eem_bin7,eem_bin8,mme_bin1,mme_bin2,mme_bin3,mme_bin4,mme_bin5,mme_bin6,mme_bin7,mme_bin8,mmm_bin1,mmm_bin2,mmm_bin3,mmm_bin4,mmm_bin5,mmm_bin6,mmm_bin7,mmm_bin8 --PO poi=fs1 --PO range_fs1=-40,40` (-40 to 40 to extrapolate the curve)   
`combine Example_WZ_fs.root -M MultiDimFit -P fs1 --floatOtherPOIs=0 --algo=grid --points=1001 --minimizerStrategy=2 -n 1Par_fs1_obs`  
`combine Example_WZ_fs.root -M MultiDimFit -P fs1 --floatOtherPOIs=0 --algo=grid --points=1001 --minimizerStrategy=2 -n 1Par_fs1_exp    --expectSignal=1 -t -1`  
`python plot1d_limit.py --POI=fs1`  

To calculate 1D limits for fs0:  
-----------------------------
Change fs1 to fs0 in config_WZ_fs (par1Name)  
Change fs0 to fs1 in config_Wz_fs (morepars)  
Change fs1 to fs0 in config_WZ_fs_bkg (par1Name)  
Change fs1 to fs0 in the instructions for fs1 above.  

To calculate 1D limits for fm1:  
----------------------------

Change path to data file at the beginning of test_fm_bin_separated.py  
`python test_fm_bin_separated.py`  
`python doFit_nonuniformbins_bin_separated.py --config=config_WZ_fm_bin_separated`   
`python buildWorkspace_AC.py --config=config_WZ_fm_bkg_bin_separated`  
`combineCards.py aC_eee_bin*.txt aC_eem_bin*.txt aC_mme_bin*.txt aC_mmm_bin*.txt > aC_WZ_all_fm_bin_separated.txt`  
`text2workspace.py -m 126 aC_WZ_all_fm_bin_separated.txt -o Example_WZ_fm_bin_separated.root -P CombinedEWKAnalysis.CommonTools.ACModel:par1_TF1_Model --PO channels=eee_bin1,eee_bin2,eee_bin3,eee_bin4,eee_bin5,eee_bin6,eee_bin7,eee_bin8,eem_bin1,eem_bin2,eem_bin3,eem_bin4,eem_bin5,eem_bin6,eem_bin7,eem_bin8,mme_bin1,mme_bin2,mme_bin3,mme_bin4,mme_bin5,mme_bin6,mme_bin7,mme_bin8,mmm_bin1,mmm_bin2,mmm_bin3,mmm_bin4,mmm_bin5,mmm_bin6,mmm_bin7,mmm_bin8 --PO poi=fm1 --PO range_fm1=-30,30`  
`combine Example_WZ_fm_bin_separated.root -M MultiDimFit -P fm1 --floatOtherPOIs=0 --algo=grid --points=1001 --minimizerStrategy=2 -n 1Par_fm1_obs`  
`combine Example_WZ_fm_bin_separated.root -M MultiDimFit -P fm1 --floatOtherPOIs=0 --algo=grid --points=1001 --minimizerStrategy=2 -n 1Par_fm1_exp  --expectSignal=1 -t -1`  
`python plot1d_limit.py --POI=fm1`  

To calculate 1D limits for fm0: 
----------------------------
Analogous to fs0  


To calculate 1D limits for ft1: 
----------------------------

Change path to data file at the beginning of test_ft.py   
`python test_ft.py`  
`python doFit_nonuniformbins_bin_separated.py --config=config_WZ_ft`   
`python buildWorkspace_AC.py --config=config_WZ_ft_bkg`   
`combineCards.py aC_eee_bin*.txt aC_eem_bin*.txt aC_mme_bin*.txt aC_mmm_bin*.txt > aC_WZ_all_ft.txt`  
`text2workspace.py -m 126 aC_WZ_all_ft.txt -o Example_WZ_ft.root -P CombinedEWKAnalysis.CommonTools.ACModel:par1_TF1_Model --PO channels=eee_bin1,eee_bin2,eee_bin3,eee_bin4,eee_bin5,eee_bin6,eee_bin7,eee_bin8,eem_bin1,eem_bin2,eem_bin3,eem_bin4,eem_bin5,eem_bin6,eem_bin7,eem_bin8,mme_bin1,mme_bin2,mme_bin3,mme_bin4,mme_bin5,mme_bin6,mme_bin7,mme_bin8,mmm_bin1,mmm_bin2,mmm_bin3,mmm_bin4,mmm_bin5,mmm_bin6,mmm_bin7,mmm_bin8 --PO poi=ft1 --PO range_ft1=-2,2`    
`combine Example_WZ_ft.root -M MultiDimFit -P ft1 --floatOtherPOIs=0 --algo=grid --points=1001 --minimizerStrategy=2 -n 1Par_ft1_obs`    
`combine Example_WZ_ft.root -M MultiDimFit -P ft1 --floatOtherPOIs=0 --algo=grid --points=1001 --minimizerStrategy=2 -n 1Par_ft1_exp  --expectSignal=1 -t -1`  
`python plot1d_limit.py --POI=ft1`  

To calculate 1D limits for ft0/ft2:
---------------------------------
Analogous to fs0


To calculate 2D limits for fs: 
-----------------------------
`python test_fs.py`  
`python doFit_nonuniformbins_bin_separated.py --config=config_WZ_fs_2D`   
`python buildWorkspace_AC.py --config=config_WZ_fs_bkg_2D`   
`combineCards.py aC_eee_bin*.txt aC_eem_bin*.txt aC_mme_bin*.txt aC_mmm_bin*.txt > aC_WZ_all_fs.txt`  
`text2workspace.py -m 126 aC_WZ_all_fs.txt -o Example_WZ_fs.root -P CombinedEWKAnalysis.CommonTools.ACModel:par1par2_TF2_Model --PO channels=eee_bin1,eee_bin2,eee_bin3,eee_bin4,eee_bin5,eee_bin6,eee_bin7,eee_bin8,eem_bin1,eem_bin2,eem_bin3,eem_bin4,eem_bin5,eem_bin6,eem_bin7,eem_bin8,mme_bin1,mme_bin2,mme_bin3,mme_bin4,mme_bin5,mme_bin6,mme_bin7,mme_bin8,mmm_bin1,mmm_bin2,mmm_bin3,mmm_bin4,mmm_bin5,mmm_bin6,mmm_bin7,mmm_bin8 --PO poi=fs0,fs1 --PO range_fs0=-50,50 --PO range_fs1=-50,50`  
`combine Example_WZ_fs.root -M MultiDimFit -P fs0 -P fs1 --floatOtherPOIs=0 --algo=grid --points=1001 --minimizerStrategy=2 -n _fs_2D`  
`mv higgsCombine_fs_2D.MultiDimFit.mH120.root higgsCombineTest.MultiDimFit.mH120_measured.root`  
`combine Example_WZ_fs.root -M MultiDimFit -P fs0 -P fs1 --floatOtherPOIs=0 --algo=grid --points=1001 --minimizerStrategy=2 -n _fs_2D --expectSignal=1 -t -1`  
`mv higgsCombine_fs_2D.MultiDimFit.mH120.root higgsCombineTest.MultiDimFit.mH120_expected.root`  
`root -l atgcplotLimit_bestfit.C+`  

To calculate 2D limits for fm:    
-----------------------------  
`python test_fm_bin_separated.py`  
`python doFit_nonuniformbins_bin_separated.py --config=config_WZ_fm_2D`  
`python buildWorkspace_AC.py --config=config_WZ_fm_bkg_2D`  
`combineCards.py aC_eee_bin*.txt aC_eem_bin*.txt aC_mme_bin*.txt aC_mmm_bin*.txt > aC_WZ_all_fm_bin_separated.txt`  
`text2workspace.py -m 126 aC_WZ_all_fm_bin_separated.txt -o Example_WZ_fm.root -P CombinedEWKAnalysis.CommonTools.ACModel:par1par2_TF2_Model --PO channels=eee_bin1,eee_bin2,eee_bin3,eee_bin4,eee_bin5,eee_bin6,eee_bin7,eee_bin8,eem_bin1,eem_bin2,eem_bin3,eem_bin4,eem_bin5,eem_bin6,eem_bin7,eem_bin8,mme_bin1,mme_bin2,mme_bin3,mme_bin4,mme_bin5,mme_bin6,mme_bin7,mme_bin8,mmm_bin1,mmm_bin2,mmm_bin3,mmm_bin4,mmm_bin5,mmm_bin6,mmm_bin7,mmm_bin8 --PO poi=fm0,fm1 --PO range_fm0=-16,16 --PO range_fm1=-60,60`  
`combine Example_WZ_fm.root -M MultiDimFit -P fm0 -P fm1 --floatOtherPOIs=0 --algo=grid --points=1001 --minimizerStrategy=2 -n _fm_2D`  
`mv higgsCombine_fm_2D.MultiDimFit.mH120.root higgsCombineTest.MultiDimFit.mH120_measured.root`  
`combine Example_WZ_fm.root -M MultiDimFit -P fm0 -P fm1 --floatOtherPOIs=0 --algo=grid --points=1001 --minimizerStrategy=2 -n _fm_2D --expectSignal=1 -t -1`  
`mv higgsCombine_fm_2D.MultiDimFit.mH120.root higgsCombineTest.MultiDimFit.mH120_expected.root`  
`root -l atgcplotLimit_bestfit.C+`  

To calculate 2D limits for ft:     
-----------------------------  
`python test_ft.py`  
`python doFit_nonuniformbins_bin_separated.py --config=config_WZ_ft_2D`  
`python buildWorkspace_AC.py --config=config_WZ_ft_bkg_2D`   
`combineCards.py aC_eee_bin*.txt aC_eem_bin*.txt aC_mme_bin*.txt aC_mmm_bin*.txt > aC_WZ_all_ft.txt`  
`text2workspace.py -m 126 aC_WZ_all_ft.txt -o Example_WZ_ft.root -P CombinedEWKAnalysis.CommonTools.ACModel:par1par2_TF2_Model --PO channels=eee_bin1,eee_bin2,eee_bin3,eee_bin4,eee_bin5,eee_bin6,eee_bin7,eee_bin8,eem_bin1,eem_bin2,eem_bin3,eem_bin4,eem_bin5,eem_bin6,eem_bin7,eem_bin8,mme_bin1,mme_bin2,mme_bin3,mme_bin4,mme_bin5,mme_bin6,mme_bin7,mme_bin8,mmm_bin1,mmm_bin2,mmm_bin3,mmm_bin4,mmm_bin5,mmm_bin6,mmm_bin7,mmm_bin8 --PO poi=ft0,ft1 --PO range_ft0=-2,2 --PO range_ft1=-2,2`  
`combine Example_WZ_ft.root -M MultiDimFit -P ft0 -P ft1 --floatOtherPOIs=0 --algo=grid --points=1001 --minimizerStrategy=2 -n _ft_2D`  
`mv higgsCombine_ft_2D.MultiDimFit.mH120.root higgsCombineTest.MultiDimFit.mH120_measured.root`  
`combine Example_WZ_ft.root -M MultiDimFit -P ft0 -P ft1 --floatOtherPOIs=0 --algo=grid --points=1001 --minimizerStrategy=2 -n _ft_2D --expectSignal=1 -t -1`  
`mv higgsCombine_ft_2D.MultiDimFit.mH120.root higgsCombineTest.MultiDimFit.mH120_expected.root`  
`root -l atgcplotLimit_bestfit.C+`  

