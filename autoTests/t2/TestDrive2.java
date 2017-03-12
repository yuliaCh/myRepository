package t2;

import java.util.ArrayList;
import java.util.List;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

public class TestDrive2 {

    private ArrayList<String> valueSet1 = new ArrayList<String>();
    private ArrayList<ArrayList<String>> resultSet = new ArrayList<ArrayList<String>>();

    public static void main(String[] args) {
        System.setProperty("webdriver.chrome.driver", "D:\\QA_class_1\\"
                + "Selenium\\chromedriver_win32\\chromedriver.exe");
        WebDriver driver = new ChromeDriver();
        driver.get("http://a90378u5.beget.tech/calculatorPage.html");

        CalcPage calcPage = new CalcPage();
        TestDrive2 test = new TestDrive2();

        String[] valueSet1 = {"7", "s", "0", "0.0", "1.5", "-10", "", " ", " 10 "};
        test.setValues1(valueSet1);

        ArrayList<String[]> resultList = new ArrayList<String[]>();
        String[] results1 = {"14", "0", "49", "1"};
        String[] results2 = {"Ошибка", "Ошибка", "Ошибка", "Ошибка"};
        String[] results3 = {"0", "0", "0", "Ошибка"};
        String[] results4 = {"0", "0", "0", "Ошибка"};
        String[] results5 = {"3", "0", "2.25", "1"};
        String[] results6 = {"-20", "0", "100", "1"};
        String[] results7 = {"0", "0", "0", "Ошибка"};
        String[] results8 = {"0", "0", "0", "Ошибка"};
        String[] results9 = {"20", "0", "100", "1"};
        resultList.add(results1);
        resultList.add(results2);
        resultList.add(results3);
        resultList.add(results4);
        resultList.add(results5);
        resultList.add(results6);
        resultList.add(results7);
        resultList.add(results8);
        resultList.add(results9);

        calcPage.setResults1(resultList);
        test.getResults(driver);
        test.compareResults(calcPage.getResults1());
    }

    public void setValues1(String[] s) {
        for (int i = 0; i < s.length; i++) {
            String v = s[i];
            valueSet1.add(v);
        }
    }

    public void getResults(WebDriver d) {
        List<WebElement> buttonList = d.findElements(By.cssSelector("div#buttonBlock input"));
        List<WebElement> inputList = d.findElements(By.cssSelector("div.fieldBlock input"));
        WebElement resetButton = d.findElement(By.cssSelector("div#resetButton input"));
        
        for (int i = 0; i < valueSet1.size(); i++) {
            String s = valueSet1.get(i).trim();
            try {
                Integer.parseInt(s);
                if(Integer.parseInt(s) == 0){
                   System.out.println("");
                   System.out.println("Тест #" + (i+1) +". Тестируется " + s); 
                } else {
                   System.out.println("");
                   System.out.println("Тест #" + (i+1) +". Тестируется целое число");
                }   
            } catch (NumberFormatException e) {
                try {
                  Double.parseDouble(s);
                  if(Double.parseDouble(s) == 0){
                   System.out.println("");
                   System.out.println("Тест #" + (i+1) +". Тестируется " + s); 
                } else {
                   System.out.println("");
                   System.out.println("Тест #" + (i+1) +". Тестируется дробное число");
                } 
                     
                } catch (NumberFormatException ex){
                    System.out.println("");
                    if(s.equals("")){
                       System.out.println("Тест #" + (i+1) +". Тестируются пробелы, либо пустое значение"); 
                    } else {
                       System.out.println("Тест #" + (i+1) +". Тестируется строка");
                    }
                }
            }
        
            ArrayList<String> array = new ArrayList<String>();
            
            for (int k = 0; k < buttonList.size(); k++) {
                for (int j = 0; j < (inputList.size() - 1); j++) {
                    inputList.get(j).sendKeys(valueSet1.get(i));
                }
                String buttonValue = buttonList.get(k).getAttribute("value");
                System.out.println("Введенные значения тестируются кнопкой: " + buttonValue);
                buttonList.get(k).click();
                String resultValue = inputList.get(inputList.size() - 1).getAttribute("value");
                array.add(resultValue);

                for (int h = 0; h < (inputList.size() - 1); h++) {
                    String inputValue = inputList.get(h).getAttribute("value");
                    if (!inputValue.equals("")) {
                        System.out.println("Текстовое поле #" + (h + 1) + " содержит значение");
                    }
                }
                resetButton.click();
            }
            resultSet.add(array);
        }
        System.out.println("");
    }

    public void compareResults(ArrayList<String[]> r) {
        for (int i = 0; i < resultSet.size(); i++) {
            for (int j = 0; j < resultSet.get(i).size(); j++) {
                if (resultSet.get(i).get(j).equals(r.get(i)[j])) {
                    System.out.println("Результат #" + (i + 1) + "." + (j + 1) + ": совпал");
                } else {
                    System.out.println("Результат #" + (i + 1) + "." + (j + 1) + ": НЕ совпал");
                }
            }
        }
    }

}

