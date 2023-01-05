#include "TCanvas.h"
#include "TFrame.h"
#include "TGraphErrors.h"

void fit_data()
{
  TCanvas *c1 = new TCanvas("c1","A Simple Graph with error bars",200,10,700,500);
  c1->SetFillColor(42);
  c1->SetGrid();
  c1->GetFrame()->SetFillColor(21);
  c1->GetFrame()->SetBorderSize(12);
  const Int_t n = 3;
  Double_t x[n]  = { 1.0, 2.0, 3.0 };
  Double_t y[n]  = { 4.308, 5.249, 5.045 };
  Double_t ex[n] = { 0.0, 0.0, 0.0 };
  Double_t ey[n] = { 0.521, 0.181, 0.092 };
  TGraphErrors *gr = new TGraphErrors(n,x,y,ex,ey);
  gr->Fit("pol0");
  gr->SetTitle("TGraphErrors Example");
  gr->SetMarkerColor(4);
  gr->SetMarkerStyle(21);
  gr->Draw("ALP");

  return;
} 
