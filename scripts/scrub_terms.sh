#!/bin/bash
set -euo pipefail

echo "Scrubbing text files for unwanted terms…"
patterns='*.py *.md *.txt *.rst *.tex *.json *.yaml *.yml *.ipynb'
for term in 'torus theory' 'halcyon'; do
  for f in $(git ls-files $patterns); do
    grep -qi "$term" "$f" && {
      echo "removing '$term' from $f"
      sed -i "s/${term}//Ig" "$f"
      git add "$f"
    }
  done
done

git diff --cached --quiet || {
  git commit -m "Docs/Code: remove stray TORUS/Halcyon references"
  git push
}
