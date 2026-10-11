import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.StringTokenizer;

public final class Main {
    static final long MOD = 1_000_000_007L;

    static final class Input {
        final int syllablesPerLine;
        final int[] wordSyllables;
        final int[] rhymeClasses;
        final int[] schemeFrequency;

        Input(int syllablesPerLine, int[] wordSyllables,
              int[] rhymeClasses, int[] schemeFrequency) {
            this.syllablesPerLine = syllablesPerLine;
            this.wordSyllables = wordSyllables;
            this.rhymeClasses = rhymeClasses;
            this.schemeFrequency = schemeFrequency;
        }
    }

    static long countPoems(Input input) {
        // TASK 1: Count ordered word sequences for each attainable syllable total.
        // TASK 2: Count complete lines by the rhyme class of their final word.
        // TASK 3: Combine line choices for each repeated scheme letter modulo MOD.
        // Different scheme letters may choose the same rhyme class.
        throw new UnsupportedOperationException("The poem counter is unfinished.");
    }

    private static int integer(StringTokenizer tokens, int low, int high) {
        if (!tokens.hasMoreTokens()) {
            throw new IllegalArgumentException("An input integer is missing.");
        }
        int value;
        try {
            value = Integer.parseInt(tokens.nextToken());
        } catch (NumberFormatException error) {
            throw new IllegalArgumentException("An input token is not an integer.", error);
        }
        if (value < low || value > high) {
            throw new IllegalArgumentException("An input integer is outside its bounds.");
        }
        return value;
    }

    static Input readInput(String text) {
        StringTokenizer tokens = new StringTokenizer(text);
        int wordCount = integer(tokens, 1, 5_000);
        int lineCount = integer(tokens, 1, 100_000);
        int syllables = integer(tokens, 1, 5_000);
        int[] wordSyllables = new int[wordCount];
        int[] rhymeClasses = new int[wordCount];
        for (int i = 0; i < wordCount; i++) {
            wordSyllables[i] = integer(tokens, 1, syllables);
            rhymeClasses[i] = integer(tokens, 1, wordCount) - 1;
        }
        int[] schemeFrequency = new int[26];
        for (int i = 0; i < lineCount; i++) {
            if (!tokens.hasMoreTokens()) {
                throw new IllegalArgumentException("A scheme letter is missing.");
            }
            String letter = tokens.nextToken();
            if (letter.length() != 1 || letter.charAt(0) < 'A' || letter.charAt(0) > 'Z') {
                throw new IllegalArgumentException("Scheme letters must be uppercase A through Z.");
            }
            schemeFrequency[letter.charAt(0) - 'A']++;
        }
        if (tokens.hasMoreTokens()) {
            throw new IllegalArgumentException("Unexpected trailing input.");
        }
        return new Input(syllables, wordSyllables, rhymeClasses, schemeFrequency);
    }

    public static void main(String[] args) {
        try {
            Input input = readInput(Files.readString(Path.of("poetry.in"), StandardCharsets.UTF_8));
            long answer = countPoems(input);
            if (answer < 0 || answer >= MOD) {
                throw new IllegalArgumentException("The answer must be normalized modulo MOD.");
            }
            Files.writeString(Path.of("poetry.out"), answer + "\n", StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println(error.getMessage());
            System.exit(2);
        }
    }
}
