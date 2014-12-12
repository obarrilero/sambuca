''' Sambuca Sensor Filtering
'''
import math
import numpy as np


def apply_sensor_filter(spectra, filter):
    # Filtsum is the area under each bands spectral reponse in filt, calculated
    # as in my fortran version below and in the McMC matlab code. This whole process of spectral resampling is
    # done using a native function in IDL, so I had to work out a way to do it
    # here. It may not be the most effective or efficient, and i'm not sure it
    # will work if the spectral filter (filt) is not normalised to 1 as it is
    # here.
    #filtsum(:) = 0
    # do j=1,n_wls
    # 	do i=1, d_wls
    # 		filtsum(j) = filtsum(j)+ filt(i,j)
    # 	enddo
    # enddo
    num_bands_in = spectra.shape[0]
    num_bands_out = filter.shape[1]

    assert filter.shape[0] == num_bands_in

    filtsum = filter.sum(1)


    # This is the application of the Sensor filter, turning the full spectrum
    # modelled data into the spectral response (filt) of the sensor (in this
    # case 551 1nm bands, to 36 bands). The synthetic sensor data I created for
    # my tests is 36 bands each 10nm wide with a constant repsonse over those
    # 10nm (see the shape of filt). A real sesnor will have more complex shape,
    # but the concept is the same
    # for j=1:n_wls
        # for i=1:d_wls
            # calc(i,j) = rrs(i) * filt(i,j);
            # bandsum(j) = bandsum(j)+ calc(i,j);
        # end
    # end


    # for i=1:n_wls
        # calcspec(i) = bandsum(i)/filtsum(i);
    # end

    return None
