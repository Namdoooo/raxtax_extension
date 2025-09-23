use std::process::exit;
use std::path::PathBuf;
use crate::parser;
use crate::tree::Tree;
use crate::utils;

use pyo3::prelude::*;

pub fn is_correct_oriented(kmers: &Vec<u16>, tree: &Tree) -> bool {
    let mut sum: i32 = 0;

    for &kmer in kmers {
        sum += tree.k_mer_map[kmer as usize].len() as i32;
        sum -= tree.k_mer_map[!kmer as usize].len() as i32;
    }

    sum >= 0
}

pub fn compute_intersections(
    queries: &Vec<(String, Vec<u16>)>,
    tree: &Tree,
) -> Vec<(String, u32, Vec<u16>)> {
    queries
        .iter()
        .map(|(label, kmers)| {
            let mut intersect_buffer = vec![0u16; tree.num_tips];

            for &kmer in kmers {
                for &ref_idx in &tree.k_mer_map[kmer as usize] {
                    intersect_buffer[ref_idx as usize] += 1;
                }
            }

            (label.clone(), kmers.len() as u32, intersect_buffer)
        })
        .collect()
}


pub fn parse_input(reference_path_str: &str, query_path_str: &str, complement: bool) -> PyResult<(Vec<(String, u32, Vec<u16>)>, Vec<u32>, Vec<String>)> {

    // Parse reference databse    
    let reference_path = PathBuf::from(reference_path_str);
    let (_, tree) =
    parser::parse_reference_fasta_file(&reference_path).unwrap_or_else(|e| {
        utils::report_error(
            e,
            format!("Failed to parse {}", reference_path.display()),
        );
        exit(exitcode::NOINPUT);
    });

    // Parse queries
    let query_path = PathBuf::from(query_path_str);
    let queries = parser::parse_query_fasta_file(&query_path).unwrap_or_else(|e| {
        utils::report_error(e, format!("Failed to parse {}", query_path.display()));
        exit(exitcode::NOINPUT);
    });

    let query_kmer_sets: Vec<(String, Vec<u16>)> = queries
        .into_iter()
        .map(|(label, sequence)| {
            let kmers = utils::sequence_to_kmers(&sequence);
            (label, kmers)
        })
        .collect();

    let oriented_query_kmer_sets: Vec<(String, Vec<u16>)> = query_kmer_sets
        .into_iter()
        .map(|(label, kmers)| {
            if is_correct_oriented(&kmers, &tree) || !complement {
                (label, kmers)
            } else {
                let complement_kmers = kmers.iter().map(|&kmer| !kmer).rev().collect();
                (label, complement_kmers)
            }
        })
        .collect();

    let mut reference_set_sizes = vec![0u32; tree.num_tips];
    for sequence_ids in &tree.k_mer_map {
        for &id in sequence_ids {
            reference_set_sizes[id as usize] += 1;
        }
    }

    Ok((compute_intersections(&oriented_query_kmer_sets, &tree), reference_set_sizes, tree.lineages))
}