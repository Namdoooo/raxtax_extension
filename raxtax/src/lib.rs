pub mod io;
pub mod lineage;
pub mod parser;
pub mod prob;
pub mod raxtax;
pub mod tree;
pub mod utils;
pub mod rust_utils;

use pyo3::prelude::*;

#[pyfunction]
fn parse_input1(reference_path_str: &str, query_path_str: &str, complement: bool) -> PyResult<(Vec<(String, u32, Vec<u16>)>, Vec<u32>, Vec<String>)> {
    rust_utils::parse_input(reference_path_str, query_path_str, complement)
}

#[pymodule]
fn rust_bindings(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse_input1, m)?)?;
    Ok(())
}