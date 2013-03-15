/**
 * @file t1.cpp
 *
 * @brief 
 *
 * @details 
 *
 * @version 1.0
 * @date 2012年04月25日 16时00分42秒
 *
 * @author 
 */

class D : public B // B needs to be defined
{
  private:
    C *ptr_c; // a pointer/reference to C can be used as C has been forward declared
    double x = 12.3; // C++11 inline data member initialization
    static const int sci = 1; // this is valid in C++98 as well
  public:
    typedef B parent_type;
 
    // inline function
    virtual parent_type foo() const
    {
        return B();
    }
 
    // non-inline function declaration. needs to be defined externally
    void bar();
} D_obj; // An object of type D is defined
 
// definition of a class method outside the class
void D::bar()
{
   //...
}


struct B
{
    int i;
    int j;
}

enum color {
    red,
    yellow,
    green = 20,
    blue
};

union foo
{
  int x;
  signed char y;
};
 

int main( int argc, char** argv)
{
    return 0;
}
