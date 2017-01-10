/**
 * merge.java
 *
 * DESCRIPTION:
 *     A merge sort for List type collections
 *     of integers.
 *
 * TO USE:
 *     call merge.mergeSort() on a List type
 *     collection of ints that you need to sort.
 *
 * Java 8 | MacOS | 12/11/16
 */
import java.util.*;

public class merge {
    /**  The merge sort class */

    public static List mergeSort(List unsorted_list){
        /**
         * A static method that sorts a List type
         * collection of ints.
         * 
         * @param unsorted_list a List of ints to be sorted
         * @return a sorted version of the List that
         *         was passed.
         */
        int size = unsorted_list.size();

        if(size <= 1){
            return unsorted_list;
        }else{
            int index_right = 0;
            int index_left = 0;
            int max_right = 0;
            int max_left = 0;
            int midpoint = size/2;

            boolean merged = false;

            List<Integer> sorted_array = new ArrayList();
            List<Integer> leftSide = mergeSort(unsorted_list.subList(0,midpoint));
            List<Integer> rightSide = mergeSort(unsorted_list.subList(midpoint,size));

            max_left = leftSide.size();
            max_right = rightSide.size();

            while(merged == false){
                if((index_left < max_left) && (index_right < max_right)) { //both side need to be merged
                    if (leftSide.get(index_left) < rightSide.get(index_right)) { //lefts first value is smaller
                        sorted_array.add(leftSide.get(index_left));
                        index_left++;
                    } else if (leftSide.get(index_left) > rightSide.get(index_right)) { //right value is smaller
                        sorted_array.add(rightSide.get(index_right));
                        index_right++;
                    } else {     //equal sides
                        sorted_array.add(leftSide.get(index_left));
                        index_left++;
                        sorted_array.add(rightSide.get(index_right));
                        index_right++;
                    }
                } else if((index_left == max_left) && (index_right != max_right)) { // left is empty, right has more
                    sorted_array.add(rightSide.get(index_right));
                    index_right++;
                } else if((index_left != max_left) && (index_right == max_right)){ // right is empty, left has more
                    sorted_array.add(leftSide.get(index_left));
                    index_left++;
                } else {               // all done
                    merged = true;
                }
            }
            return sorted_array;
        }
    }
}
