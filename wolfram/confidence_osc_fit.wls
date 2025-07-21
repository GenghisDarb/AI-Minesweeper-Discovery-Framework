hist = Import["data/confidence_history.csv"]; (* one column, 0-1 range *)
t = Range@Length@hist;
model = a + b Exp[-λ t] Cos[2 Pi t/τ + φ];
fit = NonlinearModelFit[Transpose[{t, hist}], model,
{{a, 0.5}, {b, 0.25}, {λ, 0.05}, {τ, 14}, {φ, 0}}, t];
params = Normal[fit["BestFitParameters"]];
Export["data/confidence_fit_params.json", KeyMap[ToString, params], "JSON"];
Plot[{hist, Evaluate[fit[t]]}, {t, 1, Length@hist},
PlotLegends -> {"data", "damped χ-wave"}] //
Export["figures/confidence_fit.png", #, "PNG"] &
