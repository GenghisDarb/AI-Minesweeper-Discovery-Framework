Needs["UtilitiesParallelUtilities"];
Map[
RunProcess[{"wolframscript", "-file", #}, "StandardOutput"] &,
{
"wolfram/chi_precision.wls",
"wolfram/torus_brot_scaling.wls",
"wolfram/prime_residue_scan.wls",
"wolfram/confidence_osc_fit.wls"
}
]
