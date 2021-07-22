echo -e '1abracadabraarbadacarba1\n2abracadabraarbadacarba2\n3abracadabraarbadacarba3' |
  nc 20.51.215.194 1337 |
  grep -o 'ictf.*' |
  tee >(clip.exe) # wsl ftw
