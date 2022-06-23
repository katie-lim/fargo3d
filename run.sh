#!/bin/sh

reset=true
if [ "$reset" = true ]
then
    echo "Resetting."
    rm outputs/$1/*

    # Run the simulation with the planets fixed
    echo "Starting simulation with fixed planets."
    ./fargo3d setups/fargo/fixed/$1_fixed.par &
    wait

    # Restart the simulation from the last output file
    last_output=$(ls outputs/$1/gasdens*.dat | sed "s~outputs/$1/gasdens~~" | sed "s~.dat~~" | sort -V | tail -1)
    echo "Releasing planets. Restarting simulation from output $last_output"
    ./fargo3d -S $last_output setups/fargo/$1.par
else
    echo "Restarting."
    last_output=$(ls outputs/$1/gasdens*.dat | sed "s~outputs/$1/gasdens~~" | sed "s~.dat~~" | sort -V | tail -1)
    echo "Restarting simulation from output $last_output"

    ./fargo3d -S $last_output setups/fargo/fixed/$1_fixed.par &
    wait
    ./fargo3d -S $last_output setups/fargo/$1.par
fi

