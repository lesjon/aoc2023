import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

public class Main {
    public static void main(String[] args) throws IOException {
        var file = Files.readString(Path.of("../input.txt"));
        System.out.println(run(file));
    }

    static long run(String text) {
        var lines = new HashMap<String, List<Integer>>();
        for (var line : text.split("\n")) {
            var parts = line.split(" ");
            List<Integer> ints = Arrays.stream(parts[1].split(",")).map(Integer::parseInt).toList();
            lines.put(parts[0], ints);
        }
        long total = 0;
        for (var line : lines.entrySet()) {
            System.out.println(line);
            List<String> possibilities = possibilities(line.getKey());
            if (!possibilities.stream().allMatch((p) -> p.length() == line.getKey().length())){
                throw new RuntimeException("Not all possibilities were same length as input");
            }
            System.out.println(possibilities.size());
            long count = possibilities.stream().filter(s -> valid(s, line.getValue())).count();
            System.out.println(count);
            total += count;
        }
        return total;
    }

    static boolean valid(String s, List<Integer> ints) {
        int current = 0;
        var actual = new ArrayList<Integer>();
        for (var c : s.toCharArray()) {
            switch (c) {
                case '#' -> current += 1;
                case '.' -> {
                    if (current > 0) {
                        actual.add(current);
                        current = 0;
                    }
                }
                default -> throw new RuntimeException("Unknown char '" + c + "'");
            }
        }
        if (current > 0) {
            actual.add(current);
        }
        return ints.equals(actual);
    }

    static List<String> possibilities(String s) {
        int q_index = s.indexOf('?');
        if (q_index == -1) {
            return List.of(s);
        }
        String current = s.substring(0, q_index);
        List<String> subs = possibilities(s.substring(q_index + 1));
        var result = new ArrayList<String>();
        for (var sub : subs) {
            result.add(current + "#" + sub);
            result.add(current + "." + sub);
        }
        return result;
    }
}