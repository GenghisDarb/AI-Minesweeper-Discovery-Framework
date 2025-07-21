chi = Log[(1 + Sqrt[5])/2] // N[#, 50] &;
Export["data/chi_50digits.txt", chi, "Text"];
Print["χ_50 = ", chi];
