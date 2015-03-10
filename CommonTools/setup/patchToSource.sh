#!/bin/sh

mv CombinedEWKAnalysis/CommonTools/interface/RooACProcessScaling_1D.h HiggsAnalysis/CombinedLimit/interface/RooACProcessScaling_1D.h
mv CombinedEWKAnalysis/CommonTools/interface/RooACProcessScaling_2D.h HiggsAnalysis/CombinedLimit/interface/RooACProcessScaling_2D.h
mv CombinedEWKAnalysis/CommonTools/interface/RooACProcessScaling_3D.h HiggsAnalysis/CombinedLimit/interface/RooACProcessScaling_3D.h
mv CombinedEWKAnalysis/CommonTools/interface/RooACSemiAnalyticPdf_1D.h HiggsAnalysis/CombinedLimit/interface/RooACSemiAnalyticPdf_1D.h
mv CombinedEWKAnalysis/CommonTools/interface/RooACSemiAnalyticPdf_2D.h HiggsAnalysis/CombinedLimit/interface/RooACSemiAnalyticPdf_2D.h
mv CombinedEWKAnalysis/CommonTools/interface/RooACSemiAnalyticPdf_3D.h HiggsAnalysis/CombinedLimit/interface/RooACSemiAnalyticPdf_3D.h

mv CombinedEWKAnalysis/CommonTools/src/RooACProcessScaling_1D.cc HiggsAnalysis/CombinedLimit/src/RooACProcessScaling_1D.cc
mv CombinedEWKAnalysis/CommonTools/src/RooACProcessScaling_2D.cc HiggsAnalysis/CombinedLimit/src/RooACProcessScaling_2D.cc
mv CombinedEWKAnalysis/CommonTools/src/RooACProcessScaling_3D.cc HiggsAnalysis/CombinedLimit/src/RooACProcessScaling_3D.cc
mv CombinedEWKAnalysis/CommonTools/src/RooACSemiAnalyticPdf_1D.cc HiggsAnalysis/CombinedLimit/src/RooACSemiAnalyticPdf_1D.cc
mv CombinedEWKAnalysis/CommonTools/src/RooACSemiAnalyticPdf_2D.cc HiggsAnalysis/CombinedLimit/src/RooACSemiAnalyticPdf_2D.cc
mv CombinedEWKAnalysis/CommonTools/src/RooACSemiAnalyticPdf_3D.cc HiggsAnalysis/CombinedLimit/src/RooACSemiAnalyticPdf_3D.cc


echo '#include "../interface/RooACProcessScaling_1D.h"' | cat - HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h > dummy && mv dummy HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h
echo '#include "../interface/RooACProcessScaling_2D.h"' | cat - HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h > dummy && mv dummy HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h
echo '#include "../interface/RooACProcessScaling_3D.h"' | cat - HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h > dummy && mv dummy HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h
echo '#include "../interface/RooACSemiAnalyticPdf_1D.h"' | cat - HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h > dummy && mv dummy HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h
echo '#include "../interface/RooACSemiAnalyticPdf_2D.h"' | cat - HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h > dummy && mv dummy HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h
echo '#include "../interface/RooACSemiAnalyticPdf_3D.h"' | cat - HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h > dummy && mv dummy HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h

sed 's/#endif/#pragma link C++ class RooACProcessScaling_1D+;\n#endif/' < HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h > dummy && mv dummy HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h
sed 's/#endif/#pragma link C++ class RooACProcessScaling_2D+;\n#endif/' < HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h > dummy && mv dummy HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h
sed 's/#endif/#pragma link C++ class RooACProcessScaling_3D+;\n#endif/' < HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h > dummy && mv dummy HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h
sed 's/#endif/#pragma link C++ class RooACSemiAnalyticPdf_1D+;\n#endif/' < HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h > dummy && mv dummy HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h
sed 's/#endif/#pragma link C++ class RooACSemiAnalyticPdf_2D+;\n#endif/' < HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h > dummy && mv dummy HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h
sed 's/#endif/#pragma link C++ class RooACSemiAnalyticPdf_3D+;\n#endif/' < HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h > dummy && mv dummy HiggsAnalysis/CombinedLimit/src/CombinedLimit_LinkDef.h




