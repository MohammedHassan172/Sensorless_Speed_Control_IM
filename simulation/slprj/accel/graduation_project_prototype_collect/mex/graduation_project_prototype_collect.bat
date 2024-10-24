@echo off
set skipSetupArg=%1
if "%skipSetupArg%" NEQ "skip_setup_msvc" (
call "setup_msvc.bat"
)

call  "\\DESKTOP-UTCQ70J\D$\power 2 soft\R2023a\bin\win64\checkMATLABRootForDriveMap.exe" "\\DESKTOP-UTCQ70J\D$\power 2 soft\R2023a"  > mlEnv.txt
for /f %%a in (mlEnv.txt) do set "%%a"\n

cd .
nmake -f graduation_project_prototype_collect.mk MATLAB_ROOT=%MATLAB_ROOT% ALT_MATLAB_ROOT=%ALT_MATLAB_ROOT% MATLAB_BIN=%MATLAB_BIN% ALT_MATLAB_BIN=%ALT_MATLAB_BIN%  OPTS="-DTID01EQ=0"
@if errorlevel 1 goto error_exit
exit 0

:error_exit
echo The make command returned an error of %errorlevel%
exit 1