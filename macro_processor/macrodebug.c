#include <stdio.h>
#ifdef _DEBUG_
    int bugs = 0;
    #define error(msg) {printf(msg); bug++;}
#endif

#define max(a, b) (a>b?a:b)
#define min(a, b) (a<b?a:b)

int main() {
  int x = max(3,5);
  int y = min(3,5);
  printf("max(3,5)=%d\n",x);
  printf("min(3,5)=%d\n",y);
#ifdef _DEBUG_
  if (x!=5) 
    error("max(3,5)");
  if (y!=3) 
    error("min(3,5)");
  printf("共有%d個錯誤",bugs);
#endif
}