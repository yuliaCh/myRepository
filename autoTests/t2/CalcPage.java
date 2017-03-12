
package t2;

import java.util.ArrayList;


public class CalcPage {
    private ArrayList<String[]> resultList1 = new ArrayList<String[]>();
    
    public void setResults1(ArrayList<String[]> a) {
        for(int i=0;i<a.size(); i++) {
           resultList1.add(a.get(i)); 
        }
    }
    
    public ArrayList<String[]> getResults1() {
        return resultList1;
    }
}
