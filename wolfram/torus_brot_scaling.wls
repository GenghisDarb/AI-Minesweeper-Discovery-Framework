maxIter = 512;
escapeRad = 4.;
gridPts = 400;

rotPhase = Exp[2 Pi I/14]; (* χ-phase rotation *)

torusStep[z_, c_] := (Abs[Re@z] + I Abs[Im@z])^2 * rotPhase + c;

escapeIter[c_?NumericQ] := Module[{z = 0. + 0. I},
Do[z = torusStep[z, c]; If[Abs[z] > escapeRad, Return[i]], {i, maxIter}];
maxIter
];

img = Table[
escapeIter[x + I y],
{y, -2, 2, 4./gridPts}, {x, -2, 2, 4./gridPts}
] // ArrayPlot[#, ColorFunction -> "Inferno", ImageSize -> 450] &;

Export["figures/torus_brot_demo.png", img, "PNG"];

powSpec = Abs[Fourier[Total@img, FourierParameters -> {1, -1}]];
peakPos = Ordering[powSpec, -4];
Export["data/torus_brot_fft_peaks.csv", peakPos, "CSV"];
