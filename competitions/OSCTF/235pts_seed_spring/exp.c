#include <stdio.h>
#include <stdlib.h>
#include <time.h>
 
int main(){
    int r;
    srand(time(0));
    for(int i = 0; i < 30; ++i){
        r = rand() & 0xf;
        printf("%d\n", r);
    }    
}