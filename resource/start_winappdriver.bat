@echo off
::最小化运行
%1(start /min cmd.exe /c %0 :&exit)
::获取管理员权限
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
goto UACPrompt
) else ( goto gotAdmin )
:UACPrompt
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
"%temp%\getadmin.vbs"
exit /B
:gotAdmin
if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )

::关闭windows防火墙
netsh advfirewall set allprofiles state off
::设置4723端口规则

::查询ip地址
ipconfig 
for /f "tokens=2 delims=:" %%i in ('ipconfig^|findstr "IPv4 地址"') do set ip=%%i
@echo ==================[IP:%ip%]===============
::开启winappdriver服务
cd C:\
cd winappdriver
WinAppDriver.exe %ip% 4723
pause
