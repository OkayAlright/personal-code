my $HEIGHT = 10;
my $WIDTH = 10;
my @board = (loop { (loop {0})[0..10]})[0..10];

sub main(){
    my $living = True;
    while(living){
        resolve_board;
        clean_board;
    }
}

sub 

sub resolve_board(){
    my @indexShift = ((-1, 0), (-1, -1), (0, 1), (0, 0), (0, -1), (0, 1), (1, 0), (1, -1), (1, 1));
    loop(my $x = 0; $x <= WIDTH; $x++){
        loop(my @y = 0; @y <= HEIGHT; @y++){
            
