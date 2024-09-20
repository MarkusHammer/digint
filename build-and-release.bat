@echo off

SET ERROR=""
SET modulename=digint
SET targetpyver=3.12

REM NOTE THIS MUST BE BUILT USING A VERSION OF PYTHON >= 3.10, 3.9.1 and 3.8.7 #THX https://github.com/pypa/build/issues/255#issuecomment-794560752
REM below are the commands used on windows, feel free to use the most up to date version of python when possible

ECHO The following expects that the current directory is the root of this repository, and that the git repo is already initialised
PAUSE

IF NOT EXIST "./%modulename%" GOTO :error

IF NOT EXIST "./reports" MKDIR "./reports"

echo _____PIP INSTALL_____
py -%targetpyver% -m pip install pipreqs validate-pyproject[all] build twine setuptools coverage pdoc3 pyright pylint flake8 || GOTO :error

echo _____VALIDATE PYPROJECT_____
py -%targetpyver% -m validate_pyproject -vv pyproject.toml -E setuptools distutils || GOTO :error

echo _____UNITTEST 3.7_____
py -3.7 -m unittest -v 2> "./reports/UNITTEST_py3.7.txt" || GOTO :error
echo _____UNITTEST 3.10_____
py -3.10 -m unittest -v 2> "./reports/UNITTEST_py3.10.txt" || GOTO :error
echo _____UNITTEST 3.11_____
py -3.11 -m unittest -v 2> "./reports/UNITTEST_py3.11.txt" || GOTO :error
echo _____UNITTEST 3.12_____
py -3.12 -m unittest -v 2> "./reports/UNITTEST_py3.12.txt" || GOTO :error

echo _____PYRIGHT_____
py -%targetpyver% -m pyright --warnings > "./reports/PYRIGHT.txt" || GOTO :error
echo _____PYLINT_____
py -%targetpyver% -m pylint -d all -e F,E,W --reports=y --output-format=text "%modulename%" > "./reports/PYLINT.txt" | GOTO :error
echo _____FLAKE8_____
py -%targetpyver% -m flake8 --count --format pylint --tee --output-file "./reports/FLAKE8.txt" || GOTO :error

echo _____COVERAGE_____
py -%targetpyver% -m coverage run -m unittest discover || GOTO :error
(echo # COVERAGE & echo. ) > "./reports/COVERAGE.md" || GOTO :error
py -%targetpyver% -m coverage report --format=markdown >> "./reports/COVERAGE.md" || GOTO :error

echo _____PIPREQS_____
py -%targetpyver% -c "from pipreqs.pipreqs import main; main()" --mode gt --debug --force || GOTO :error

echo _____PDOC_____
py -%targetpyver% -m pdoc --html -f -c show_inherited_members=True -c list_class_variables_in_index=False -c show_type_annotations=True -c show_source_code=True -o tempdocs %modulename% || GOTO :error
IF EXIST "./docs" RMDIR "./docs" /q /s || GOTO :error
REN "./tempdocs/%modulename%" docs || GOTO :error
MOVE "./tempdocs/docs" . || GOTO :error
RMDIR "./tempdocs" /q /s || GOTO :error
COPY "./robotstemplate.txt" "docs/robots.txt" /a /y

echo _____BUILD_____
py -%targetpyver% -m build -v -o "./build" || GOTO :error
echo _____BUILD CHECK_____
py -%targetpyver% -m twine check "./build/*" || GOTO :error
echo _____BUILD CLEANUP_____
RMDIR "%modulename%.egg-info" /q /s || GOTO :error

echo _____GIT_____
git add -v -A || GOTO :error
git gc  --auto || GOTO :error

ECHO Also upload to pypi?
PAUSE
echo _____UPLOAD_____
py -%targetpyver% -m twine upload "./build/*" --username __token__ || GOTO :error

ECHO Complete!
GOTO :EOF

:error
ECHO Failed with error '%ERROR%' #%errorlevel%.
exit /b %errorlevel%
