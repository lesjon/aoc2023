use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashSet};
use std::hash::{Hash};

fn parse(text: &str) -> Vec<Vec<i32>> {
    text.lines().map(|line| line.chars().map(|i| i as i32 - '0' as i32).collect()).collect()
}

fn distance_to_target(pos: &PathNode, target: &(usize, usize)) -> usize {
    usize::abs_diff(pos.x, target.0) + usize::abs_diff(pos.y, target.1)
}

#[derive(Copy, Clone, Debug, Ord, PartialOrd, Eq, PartialEq, Hash)]
struct PathNode {
    x: usize,
    y: usize,
    dx: i32,
    dy: i32,
}

#[derive(Clone, Debug, Hash)]
struct State {
    path_node: PathNode,
    minimal_heatloss: i32,
    distance: usize,
    path: Vec<(usize, usize)>,
}

impl Eq for State {}

const ASTAR: i32 = 0;

impl PartialEq<Self> for State {
    fn eq(&self, other: &Self) -> bool {
        (other.minimal_heatloss + ASTAR * other.distance as i32).eq(&(self.minimal_heatloss + ASTAR * self.distance as i32))
    }
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        (other.minimal_heatloss + ASTAR * other.distance as i32).cmp(&(self.minimal_heatloss + ASTAR * self.distance as i32))
    }
}

impl PartialOrd<Self> for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        (other.minimal_heatloss + ASTAR * other.distance as i32).partial_cmp(&(self.minimal_heatloss + ASTAR * self.distance as i32))
    }
}

const MAX_STRAIGHT: i32 = 3;

impl State {
    fn right(&self, city_map: &Vec<Vec<i32>>) -> Option<Self> {
        if self.path_node.x + 1 == city_map[0].len() {
            return None;
        }
        if self.path_node.dx == MAX_STRAIGHT {
            return None;
        }
        if self.path_node.dx < 0 {
            return None
        }
        let x = self.path_node.x + 1;
        let y = self.path_node.y;
        let mut path = self.path.clone();
        path.push((x, y));
        Some(
            Self {
                path_node: PathNode {
                    x,
                    y,
                    dx: self.path_node.dx + 1,
                    dy: 0,
                },
                minimal_heatloss: self.minimal_heatloss + city_map[self.path_node.y][self.path_node.x + 1],
                distance: self.distance - 1,
                path,
            })
    }
    fn down(&self, city_map: &Vec<Vec<i32>>) -> Option<Self> {
        if self.path_node.y + 1 == city_map.len() {
            return None;
        }
        if self.path_node.dy == MAX_STRAIGHT {
            return None;
        }
        if self.path_node.dy < 0 {
            return None
        }
        let x = self.path_node.x;
        let y = self.path_node.y + 1;
        let mut path = self.path.clone();
        path.push((x, y));
        Some(Self {
            path_node: PathNode {
                x,
                y,
                dx: 0,
                dy: self.path_node.dy + 1,
            },
            minimal_heatloss: self.minimal_heatloss + city_map[self.path_node.y + 1][self.path_node.x],
            distance: self.distance - 1,
            path,
        })
    }
    fn left(&self, city_map: &Vec<Vec<i32>>) -> Option<Self> {
        if self.path_node.x == 0 {
            return None;
        }
        if self.path_node.dx == -MAX_STRAIGHT {
            return None;
        }
        if self.path_node.dx > 0 {
            return None
        }
        let x = self.path_node.x - 1;
        let y = self.path_node.y;
        let mut path = self.path.clone();
        path.push((x, y));
        Some(Self {
            path_node:
            PathNode {
                x,
                y,
                dx: self.path_node.dx - 1,
                dy: 0,
            },
            minimal_heatloss: self.minimal_heatloss + city_map[self.path_node.y][self.path_node.x - 1],
            distance: self.distance + 1,
            path,
        })
    }
    fn up(&self, city_map: &Vec<Vec<i32>>) -> Option<Self> {
        if self.path_node.y == 0 {
            return None;
        }
        if self.path_node.dy == -MAX_STRAIGHT {
            return None;
        }
        if self.path_node.dy > 0 {
            return None
        }
        let x = self.path_node.x;
        let y = self.path_node.y - 1;
        let mut path = self.path.clone();
        path.push((x, y));
        Some(Self {
            path_node: PathNode {
                x,
                y,
                dx: 0,
                dy: self.path_node.dy - 1,
            },
            minimal_heatloss: self.minimal_heatloss + city_map[self.path_node.y - 1][self.path_node.x],
            distance: self.distance + 1,
            path,
        })
    }

    fn next_nodes(&self, city_map: &Vec<Vec<i32>>) -> HashSet<Self> {
        let mut next_nodes = HashSet::new();
        if let Some(up) = self.up(city_map) {
            next_nodes.insert(up);
        }
        if let Some(right) = self.right(city_map) {
            next_nodes.insert(right);
        }
        if let Some(up) = self.down(city_map) {
            next_nodes.insert(up);
        }
        if let Some(up) = self.left(city_map) {
            next_nodes.insert(up);
        }
        next_nodes
    }
}

fn calc_shortest_paths(city_map: &Vec<Vec<i32>>, from: &(usize, usize), to: &(usize, usize)) -> Option<i32> {
    println!("calc_shortest_paths(from:{from:?}, to:{to:?}");
    let mut seen = HashSet::new();
    let mut simple_seen = HashSet::new();
    let mut heap = BinaryHeap::new();
    let init_pos = PathNode {
        x: from.0,
        y: from.1,
        dx: 0,
        dy: 0,
    };
    let distance = distance_to_target(&init_pos, &(city_map[0].len(), city_map.len()));
    let init = State {
        path_node: init_pos,
        minimal_heatloss: 0,
        distance,
        path: vec![(0, 0)],
    };
    heap.push(init.clone());
    seen.insert(init.path_node);
    simple_seen.insert((init.path_node.x, init.path_node.y));
    let mut min_dist = distance;

    let mut count = 0;
    while let Some(node) = heap.pop() {
        count += 1;
        let next_nodes = node.next_nodes(city_map);
        // println!("next_nodes:{:?}", next_nodes);
        let seen_clone = seen.clone();
        let filtered = next_nodes.iter().filter(move |state| !seen_clone.contains(&state.path_node));
        // println!("filtered:{:?}", filtered);
        for n in next_nodes.iter() {
            if n.distance < min_dist {
                min_dist = n.distance;
                println!("{}: new closest point {:?}, dist:{} heatloss:{}", count, n.path_node, n.distance, n.minimal_heatloss);
            }
            if n.path_node.x == to.0 && n.path_node.y == to.1 {
                for y in 0..city_map.len() {
                    for x in 0..city_map[0].len() {
                        if n.path.contains(&(x, y)) {
                            print!("#")
                        } else {
                            print!("{}", city_map[y][x])
                        }
                    }
                    println!()
                }
                return Some(n.minimal_heatloss);
            }
            seen.insert(n.path_node.clone());
            simple_seen.insert((n.path_node.x, n.path_node.y));
        }

        heap.extend(filtered.map(|s| s.clone()));
    }
    return None;
}

fn run(text: &str) -> Option<i32> {
    let city_map = parse(text);
    let target = (city_map[0].len() - 1, city_map.len() - 1);
    println!("target={target:?}");
    calc_shortest_paths(&city_map, &(0, 0), &target)
}

fn main() {
    let input = include_str!("../input.txt");
    let total = run(input);
    println!("{total:?}");
}

#[cfg(test)]
mod tests {
    use crate::run;

    #[test]
    fn test_sample() {
        let text = "2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533";
        assert_eq!(Some(102), run(text))
    }
}