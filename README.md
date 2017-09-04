setenv SCRAM_ARCH slc6_amd64_gcc481

cmsrel CMSSW_7_1_5 

cd CMSSW_7_1_5/src 

cmsenv

git clone  --branch v5.0.2 https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit

mkdir CombinedEWKAnalysis

git clone https://github.com/senka/CombinedEWKAnalysis_1D2D3D CombinedEWKAnalysis

source CombinedEWKAnalysis/CommonTools/setup/patchToSource.sh

scram b 
