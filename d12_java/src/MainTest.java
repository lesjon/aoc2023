
class MainTest {
    public static void main(String[] args) {

        String sample = """
                ???.### 1,1,3
                .??..??...?##. 1,1,3
                ?#?#?#?#?#?#?#? 1,3,1,6
                ????.#...#... 4,1,1
                ????.######..#####. 1,6,5
                ?###???????? 3,2,1""";
        if (21 != Main.run (sample)){
            throw new RuntimeException("Not Equal");

        }
    }

}