#!/bin/sh

last_output=$(ls outputs/$1/gasdens*.dat | sed "s~outputs/$1/gasdens~~" | sed "s~.dat~~" | sort -V | tail -1)
echo "Running setup with photoevaporation."
echo "Restarting simulation from output #$last_output."

./fargo3d -S $last_output setups/fargo/$1.par