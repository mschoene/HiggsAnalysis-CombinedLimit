#include "TFile.h"
#include "TMath.h"
#include "TH2D.h" 
#include "TF1.h"
#include "TProfile.h"
#include "TLegend.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TTree.h"
#include "TGraph.h"
#include "TLatex.h"
//#include "/mnt/t3nfs01/data01/shome/mschoene/80X/src/myMT2Analysis/interface/MT2DrawTools.h"
//#include "/mnt/t3nfs01/data01/shome/mschoene/80X/src/myMT2Analysis/src/MT2DrawTools.cc"


#include <iostream>

void drawMetOcaloMet(){


  gStyle->SetCanvasColor(0);
  gStyle->SetPadColor(0);
  gStyle->SetFrameFillColor(0);
  gStyle->SetStatColor(0);
  gStyle->SetOptStat(0);
  gStyle->SetTitleFillColor(0);
  gStyle->SetCanvasBorderMode(0);
  gStyle->SetPadBorderMode(0);
  gStyle->SetFrameBorderMode(0);
  gStyle->SetPadBottomMargin(0.12);
  gStyle->SetPadLeftMargin(0.12);
  gStyle->cd();
  // For the canvas:
  gStyle->SetCanvasBorderMode(0);
  gStyle->SetCanvasColor(kWhite);
  gStyle->SetCanvasDefH(600); //Height of canvas
  gStyle->SetCanvasDefW(600); //Width of canvas
  gStyle->SetCanvasDefX(0); //POsition on screen
  gStyle->SetCanvasDefY(0);
  // For the Pad:
  gStyle->SetPadBorderMode(0);
  gStyle->SetPadColor(kWhite);
  gStyle->SetPadGridX(false);
  gStyle->SetPadGridY(false);
  gStyle->SetGridColor(0);
  gStyle->SetGridStyle(3);
  gStyle->SetGridWidth(1);
  // For the frame:
  gStyle->SetFrameBorderMode(0);
  gStyle->SetFrameBorderSize(1);
  gStyle->SetFrameFillColor(0);
  gStyle->SetFrameFillStyle(0);
  gStyle->SetFrameLineColor(1);
  gStyle->SetFrameLineStyle(1);
  gStyle->SetFrameLineWidth(1);
  // Margins:
  gStyle->SetPadTopMargin(0.05);
  gStyle->SetPadBottomMargin(0.15);//0.13);
  gStyle->SetPadLeftMargin(0.15);//0.16);
  gStyle->SetPadRightMargin(0.05);//0.02);
  // For the Global title:
  gStyle->SetOptTitle(0);
  gStyle->SetTitleFont(42);
  gStyle->SetTitleColor(1);
  gStyle->SetTitleTextColor(1);
  gStyle->SetTitleFillColor(10);
  gStyle->SetTitleFontSize(0.05);
  // For the axis titles:
  gStyle->SetTitleColor(1, "XYZ");
  gStyle->SetTitleFont(42, "XYZ");
  gStyle->SetTitleSize(0.05, "XYZ");
  gStyle->SetTitleXOffset(1.15);//0.9);
  gStyle->SetTitleYOffset(1.5); // => 1.15 if exponents
  // For the axis labels:
  gStyle->SetLabelColor(1, "XYZ");
  gStyle->SetLabelFont(42, "XYZ");
  gStyle->SetLabelOffset(0.007, "XYZ");
  gStyle->SetLabelSize(0.045, "XYZ");
  // For the axis:
  gStyle->SetAxisColor(1, "XYZ");
  gStyle->SetStripDecimals(kTRUE);
  gStyle->SetTickLength(0.03, "XYZ");
  gStyle->SetNdivisions(510, "XYZ");
  gStyle->SetPadTickX(1); // To get tick marks on the opposite side of the frame
  gStyle->SetPadTickY(1);
  // for histograms:
  gStyle->SetHistLineColor(1);


  //  MT2DrawTools::setStyle();

  std::vector<std::string> list;

  //  list.push_back("sep25");
  //  list.push_back("sep26_fixedXsec");
  //  list.push_back("sep27_b012");
 
  //  list.push_back("oct10_b012V2");
  //  list.push_back("oct04_mt2bin");
  //list.push_back("oct15_isr");
  // list.push_back("oct15_isr2");
  //  list.push_back("oct15_Test");

  //  list.push_back("oct24_llbb");


  // list.push_back("nov07_bl");
  // //  list.push_back("nov07_bb");
  // list.push_back("nov12_ll_bbNew");

  // list.push_back("sep27_b012_10unc");


  // list.push_back("sep25");
  // list.push_back("sep25_lowPtCut");

  list.push_back("data2016_T2bH_2017mar12");
  list.push_back("data2016_T2bH_2017mar12_mt2");
  list.push_back("data2016_T2bH_apr12_0jsplit");

 
  std::vector<int> colors;

  
// #define kQCD 401
// #define kWJets 417
// #define kZJets 419
// #define kTop 855

// #define kQCDest 402
// #define kZinv 430
// #define kLostLepton 418

  colors.push_back( 855 );
  colors.push_back( 401 );
  colors.push_back( 417 );
  colors.push_back( 430 );


 
 

  TCanvas* canny = new TCanvas("canny","",600,600);

  TLegend* legend = new TLegend( 0.3, 0.2, 0.45, 0.45 );
  legend->SetTextSize(0.02); 
  legend->SetTextSize(0.04);
  legend->SetTextFont(42);
  legend->SetFillColor(0);
  legend->SetBorderSize(0);

  TH2D* h2_axes = new TH2D("axes", "", 10, 250, 610, 10, 0, 320 );
  h2_axes->SetStats(0);
  // h2_axes->GetXaxis()->SetLabelSize(0.00);
  //  h2_axes->GetXaxis()->SetTickLength(0.09);
  //h2_axes->GetYaxis()->SetNdivisions(5,5,0);
  //h2_axes->GetYaxis()->SetTitleSize(0.17);
  //h2_axes->GetYaxis()->SetTitleOffset(0.4);
  //h2_axes->GetYaxis()->SetLabelSize(0.17);
  h2_axes->GetYaxis()->SetTitle("m_{#chi}");
  h2_axes->GetXaxis()->SetTitle("m_{b}");
  h2_axes->Draw();

  TFile *file_razor   = TFile::Open( "CMS-SUS-16-045_Figure_005.root" );

  TGraph* g_razor   =   (TGraph*)file_razor  ->Get("expL");
  TGraph* g_razor_m   =   (TGraph*)file_razor  ->Get("expLD");
  TGraph* g_razor_p   =   (TGraph*)file_razor  ->Get("expLU");

  g_razor->SetLineWidth(2);    g_razor->SetLineColor( kBlack );
  g_razor_p->SetLineWidth(2);    g_razor_p->SetLineColor( kBlack); g_razor_p->SetLineStyle(2);
  g_razor_m->SetLineWidth(2);    g_razor_m->SetLineColor( kBlack); g_razor_m->SetLineStyle(2);


  g_razor->Draw("same");
     
  //   g_razor_p->Draw("same");    g_razor_m->Draw("same");

  legend->AddEntry(g_razor, "SUS-16-045 exp", "L" );
    


  for(unsigned int i=0; i< list.size();i++){
    
    TFile *file_g   = TFile::Open(Form("dataCards_%s/limits_SMS_T2bH_mSbottom.root",list[i].c_str() ) );
 
    // TGraph* g_g   =   (TGraph*)file_g  ->Get("gr_exp");
    // TGraph* g_g_m   =   (TGraph*)file_g  ->Get("gr_em1s");
    // TGraph* g_g_p   =   (TGraph*)file_g  ->Get("gr_ep1s");

    TGraph* g_g   =   (TGraph*)file_g  ->Get("gr_exp_smoothed");
    TGraph* g_g_m   =   (TGraph*)file_g  ->Get("gr_em1s_smoothed");
    TGraph* g_g_p   =   (TGraph*)file_g  ->Get("gr_ep1s_smoothed");


    g_g->SetLineWidth(2);    g_g->SetLineColor( colors[i] );
    g_g_p->SetLineWidth(2);    g_g_p->SetLineColor( colors[i]); g_g_p->SetLineStyle(2);
    g_g_m->SetLineWidth(2);    g_g_m->SetLineColor( colors[i]); g_g_m->SetLineStyle(2);

    g_g->Draw("same");
    //    g_g_p->Draw("same");    g_g_m->Draw("same");


    //    legend->AddEntry(g_g,  "Version 0 ", "L" );
    if(i==0)
      legend->AddEntry(g_g,  "Baseline", "L" );
    if(i==1)
      legend->AddEntry(g_g,  "W/ MT2 bins", "L" );
    if(i==2)
      legend->AddEntry(g_g,  "W/ 0j pT split", "L" );
  
  }

  
    legend->Draw("same");
    gPad->RedrawAxis();
    // canny->SaveAs( "boh/.png" );
    canny->SaveAs(Form( "comparisonLimits_apr12.eps" )  );
    canny->SaveAs(Form( "comparisonLimits_apr12.png" )  );


    // canny->SaveAs(Form( "comparisonLimits_blbbNew2.eps" )  );
    // canny->SaveAs(Form( "comparisonLimits_blbbNew2.png" )  );


    // }


}
