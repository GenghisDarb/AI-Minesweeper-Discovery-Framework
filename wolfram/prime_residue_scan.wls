Block[{n = 10^9, chunk = 10^7},
buckets = ConstantArray[0, 14];
Do[
primes = PrimeRange[k, k + chunk - 1]; (* safer than Prime[...] *)
buckets += Counts[Mod[Range[k, k + chunk - 1], 14], Range[0, 13]];
, {k, 1, n, chunk}
];
ρ = Normal@buckets;
S = Variance[ρ]/Mean[ρ] // N;
Export["reports/prime_residue_S.csv", Join[ρ, {S}], "CSV"];
Print["S-statistic = ", S];
]
