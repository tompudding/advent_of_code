use std::fs;
use std::env;

fn parse_line_part_one(line: String) -> Vec<u32>
{
    // OMG this is a monstrosity
    line.chars()
        .filter(|&x| x.is_digit(10))
        .map(|c| c.to_digit(10).unwrap())
        .collect()
}

fn parse_line_part_two(line: String) -> Vec<u32>
{
    // TODO: Implement this so it gives a different answer to part 1
    line.chars()
        .filter(|&x| x.is_digit(10))
        .map(|c| c.to_digit(10).unwrap())
        .collect()
}

fn main() {
    // Load the input
    let input = match env::args().nth(1) {
        Some(filename) => {
            match fs::read_to_string(&filename) {
                Ok(data) => data,
                Err(e) => {
                    println!("Failed to open \"{filename}\" Error=\"{e}\"");
                    return;
                },
            }
        },
        _ => {
            println!("Usage: <day_1> <input_filename>");
            return;
        },
    };

    let mut sum: u32 = 0;

    for line in input.lines() {
        let numbers: Vec<u32> = parse_line_part_one(line.into());
        sum += (numbers[0]*10) + numbers[numbers.len() - 1];
    }

    println!("part_one {sum}");

    sum = 0;

    for line in input.lines() {
        let numbers: Vec<u32> = parse_line_part_two(line.into());
        sum += (numbers[0]*10) + numbers[numbers.len() - 1];
    }

    println!("part_two {sum}");

}
