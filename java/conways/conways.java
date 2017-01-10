import java.util.*;
import java.lang.*;

public class conways{
    int HEIGHT = 49;
    int WIDTH = 85;

    int[][] board = new int[WIDTH][HEIGHT];

    int[][] index_shift = {{ 0,-1},{ 0,1},
			   { 1,-1},{ 1,0},{ 1,1},
			   {-1,-1},{-1,0},{-1,1}};

    public void prep_board(){
	for(int x = 0; x < WIDTH; x++){
	    for(int y = 0; y < HEIGHT; y++){
		board[x][y] = 2;
	    }
	}
    }

    public void resolve_board(){
	for(int y = 0; y < HEIGHT; y++){
            for(int x = 0; x < WIDTH; x++){
		switch(board[x][y]){
		case 0: //fall through
		case 3: board[x][y] = 0; break;
		case 2: //fall through
		case 1: board[x][y] = 2; break;
		}
            }
        }
    }

    public void display_board(){
	for(int y = 0; y < HEIGHT; y++){
	    System.out.print("|");
            for(int x = 0; x < WIDTH; x++){
		//System.out.format("%d ",board[x][y]);
		if(board[x][y] == 0){
		    System.out.print("o ");
		}else{
		    System.out.print("  ");
		}
	    }
	    System.out.print("| \n");
	}
	System.out.print(" ");
	for(int i = 0; i < WIDTH; i++){
	    System.out.print("- ");
	}
	System.out.print("\n\n");
    }
    
    public void eval_board(){
	    for(int x = 0; x < WIDTH; x++){
	        for(int y = 0; y < HEIGHT; y++){
		        eval_cell(x,y);
	        }
	    }
    }

    public void eval_cell(int x, int y){
	    int num_of_neighbors = count_neighbors(x,y);
	    int cell_state = board[x][y];
	// Alive = 0 dying = 1 dead = 2 birth = 3
	    if(cell_state > 1){
	        if(num_of_neighbors == 3){
		    board[x][y] = 3;
	    } else if(num_of_neighbors != 3){
		    board[x][y] = 2;
	    }
	    } else if(cell_state < 2){
	        if((num_of_neighbors == 2) || (num_of_neighbors == 3)){
		        board[x][y] = 0;
	        } else if((2 > num_of_neighbors) || (num_of_neighbors > 3)){
		        board[x][y] = 1;
	        }
	    }
    }
    
    public int count_neighbors(int x, int y){ 
	int num_of_neighbors = 0;
	for(int i = 0; i < 8; i++){
	    int[] shift = index_shift[i].clone();
            //correct wrapping
	    if((x == 0) && (shift[0] == -1)){
		shift[0] = WIDTH - 1;
	    }else if((x == WIDTH - 1) && (shift[0] == 1)){
		shift[0] = (WIDTH * -1) + 1;
	    }
	    if((y == 0) && (shift[1] == -1)){
		shift[1] = HEIGHT - 1;
	    }else if((y == HEIGHT - 1) && (shift[1] == 1)){
		shift[1] = (HEIGHT * -1) + 1;
	    }
	    //Done correcting array wrap-around.
	    if((board[x + shift[0]][y + shift[1]]) < 2){
		num_of_neighbors += 1;
	    }
	}
	return num_of_neighbors;
    }

    public static void main (String[] args){
	conways a = new conways();
	a.prep_board();
	a.board[3][3] = 0;
        a.board[3][4] = 0;
        a.board[3][5] = 0;
        a.board[4][5] = 0;
	a.board[5][4] = 0;


	a.board[30][30] = 0;
	a.board[31][30] = 0;
	a.board[32][30] = 0;
	
	while(1==1){
	    a.display_board();
	    a.eval_board();
	    a.resolve_board();
	    try {
		Thread.sleep(75);
	    } catch (Exception e) {
		System.out.println(e);
	    }
	}
    }
}
