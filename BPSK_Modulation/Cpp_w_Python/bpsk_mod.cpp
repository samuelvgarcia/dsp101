#include <iostream>
#include <fstream>
#include <bitset>
#include <vector>   // for std::vector
#include <cstdlib>  // for rand() and srand()
#include <ctime>    // for time()
#include <cmath>    // for ceil 

#define PI 3.141592653589793


// Function prototype for rand_bits 
// Input is bitset array
template<std::size_t total_bits>
void rand_bits( std::bitset<total_bits> &array);

//---------------------------------------------------------------------------------

// Main Program
int main(int argc, char *argv[]){
    // Parameters
    // Number of random bits to generate
    const int num_bits = 100;
    // Is it possible to make num_bits one of argv parameters???
    const int M = 10; // Upsamping factor
    const double fs = 500; // original sampling frequency in Hz (symbol rate)
    const double fs_new = fs*M; // new sampling frequency (5kHz) (samples that mix w/ carrier)
    
    //-------------------------------------------------
    // Create Data file for outputing data

    std::ofstream my_file;  //ofstream object

    //Argv[1] is the name of the output file
    my_file.open(argv[1]);

    //-------------------------------------------------
    // Create bit_array of random bits

    std::bitset<num_bits> bit_array; // create bitset array
    rand_bits( bit_array ); // fill with random bits

    // Write the bits to file
    for (int ii=0; ii < bit_array.size(); ii++)
        my_file << bit_array[ii] << ",";
    my_file << "\n";

    //-------------------------------------------------
    // Create BPSK symbols from bits
    // Create array of symbols

    std::vector<char> bpsk_sym (num_bits);
    
    // And do bit to symbol mapping for bpsk
    // bit 0 -> -1V, bit 1 ->+1V
    for (int ii=0; ii < bpsk_sym.size(); ii++){
        if (bit_array[ii]==1)
            bpsk_sym[ii] = 1;
        else // bit is a zero
            bpsk_sym[ii] = -1;
    }

    // Write the symbols to file
    for (int ii=0; ii < bit_array.size(); ii++)
        my_file << static_cast<int>(bpsk_sym[ii]) << ",";
    my_file << "\n";

    //-------------------------------------------------
    // Upsample the symbols

    std::vector<char> bpsk_up_samp(num_bits*M);
    for (int ii=0; ii < num_bits; ii++)
        for (int kk=0; kk<M; kk++)
            bpsk_up_samp[ii*M+kk] = bpsk_sym[ii];
    
    // Write the upsampled symbols to file
    for (int ii=0; ii < bpsk_up_samp.size(); ii++)
        my_file << static_cast<int>(bpsk_up_samp[ii]) << ",";
    my_file << "\n"; 

    //-------------------------------------------------
    // Create Carrier Freq

    double fc = 0.2 * fs_new/2; // carrier freq -> certain percentage of fs_new/2
    // Array for Carrier Cosine signal
    std::vector<double> carrier_signal ( bpsk_up_samp.size() );
    
    for (int n=0; n<bpsk_up_samp.size(); n++)
        carrier_signal[n] = cos(2*PI*fc/fs_new * n);
    
    // Write the Carrier Signal to file
    for (int ii=0; ii<carrier_signal.size(); ii++)
        my_file << carrier_signal[ii] << ",";        
    my_file << "\n";

    //-------------------------------------------------
    // Simulate Mixing and Tx signal (Analog signal)   

    // Array for Tx Signal
    std::vector<double> tx_signal (bpsk_up_samp.size());

    for (int n=0; n < bpsk_up_samp.size(); n++ )
        tx_signal[n] = bpsk_up_samp[n] * carrier_signal[n];

    // Write the TX Signal to file
    for (int ii=0; ii<carrier_signal.size(); ii++)
        my_file << tx_signal[ii] << ",";        
    my_file << "\n";    

    //-------------------------------------------------
    // Close the file

    my_file.close();

    return 0;
} // End of MAIN()

//---------------------------------------------------------------------------------
//---------------------------------------------------------------------------------
//---------------------------------------------------------------------------------

// Functions:

// Funcition body: rand_bits
template<std::size_t total_bits>
void rand_bits( std::bitset<total_bits> &array){
    
    // Random Integer between 0,15
    const int bits_per_int = 4;  //number of bits for each rand number
    const int max_int = 1 << bits_per_int;  // max range of integers [0, (2**n) - 1]
    
    // Determine number of times to go through For loop
    const int num_ints = ceil (static_cast<float>(total_bits) / bits_per_int );
    
    srand(time(0)); // seed for random
    
    for(int ii=0, x=0; ii<num_ints; ii++)
    {
        // Generate random integer between 0 and (max_int-1).  (i.e. if 4 bits, then range [0,15])
        x = rand() % max_int;
        // Alternate method:
            // x = rand()/( (RAND_MAX + 1u)/max_int );  // Note: 1+rand()%max_int is biased

        // Convert to bits, then shift into appropriate location of array
        array = array | ( std::bitset<total_bits>(x)<<(ii*bits_per_int) );

    }
    return;
}



