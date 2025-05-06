@echo off
echo Adding test files to git...
git add tests/
git add .github/workflows/
git add requirements.txt
echo Committing changes...
git commit -m "Add test automation and requirements documentation"
echo Pushing to GitHub...
git push origin feature/visual-changes-ai
echo Done!
