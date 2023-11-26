from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from herrewebpy import logger
import tqdm

"""
Multiple sequence alignment script using Needleman-Wunsch. Writes to fasta and stockholm, as well as to a plain text file.

Method derived from RP1 and RP2 internships. Used as a data validation technique in Alstom.

Author: Jonathan Herrewijnen
Email: jonathan.herrewijnen@gmail.com
Date: 25 November
Herreweb
"""


def parse_sequence(sequence):
    """
    Parse a sequence, either as a pandas DataFrame or a string, and return the result.

    Parameters:
        sequence (pd.DataFrame or str): The input sequence data to be parsed.
    """
    if sequence is None:
        return None
    elif isinstance(sequence, pd.Series):
        logger.info("Parsing data as dataframe, so converting")
        sequence = sequence.str.cat(sep='|')
    logger.info(f'Assuming type is string, returning list')
    identifiers = [item.strip('|') for item in sequence.split('|') if item.strip('|')]
    return identifiers


def write_stockholm_alignment_with_metadata(aligned_identifiers1, aligned_identifiers2, aligned_metadata1, aligned_metadata2, score, output_filename):
    """
    Write an alignment in Stockholm format with metadata as annotations.

    Parameters:
        aligned_identifiers1 (list): List of aligned identifiers for the first sequence.
        aligned_identifiers2 (list): List of aligned identifiers for the second sequence.
        aligned_metadata1 (list): List of metadata corresponding to aligned_identifiers1.
        aligned_metadata2 (list): List of metadata corresponding to aligned_identifiers2.
        score (int): Alignment score.
        output_filename (str): Name of the output Stockholm format file.

    Description:
        This function writes an alignment in the Stockholm format with custom metadata as annotations.
        It takes two lists of aligned identifiers (aligned_identifiers1 and aligned_identifiers2),
        two lists of corresponding metadata (aligned_metadata1 and aligned_metadata2), an alignment score,
        and the desired output filename.

        The function creates a Stockholm file where each sequence in the alignment is represented by its identifier.
        It includes the metadata as custom annotations (#=GC METADATA1 and #=GC METADATA2) in the Stockholm file.

        The Stockholm format is commonly used for representing sequence alignments in bioinformatics.

    Example:
        aligned_identifiers1 = ['COM12018', 'COM17003']
        aligned_identifiers2 = ['COM12018', 'COM17003']
        aligned_metadata1 = ['some_metadata', 'some_data']
        aligned_metadata2 = ['some_other_metadata', 'some_more_metadata']
        score = 42
        output_filename = 'alignment.stockholm'

        write_stockholm_alignment_with_metadata(aligned_identifiers1, aligned_identifiers2, aligned_metadata1, aligned_metadata2, score, output_filename)
    """
    with open(output_filename, 'w') as stockholm_file:
        stockholm_file.write("# STOCKHOLM 1.0\n")
        for id1, id2, metadata1, metadata2 in zip(aligned_identifiers1, aligned_identifiers2, aligned_metadata1, aligned_metadata2):
            stockholm_file.write(f"{id1}\n")
            stockholm_file.write(f"{id2}\n")
            stockholm_file.write(f"#=GC METADATA1 {metadata1}\n")
            stockholm_file.write(f"#=GC METADATA2 {metadata2}\n")
        stockholm_file.write(f"#=GF SCORE: {score}\n")


def write_text_format(aligned_identifiers1, aligned_identifiers2, score, output_filename, aligned_metadata1=None,
                        aligned_metadata2=None):
    """
    Write aligned identifiers in two seperate text files (for visual comparison)
    """
    with open(f'1-{output_filename}', 'w') as file: [file.write(f"Score: {score}\n")]
    with open(f'2-{output_filename}', 'w') as file: [file.write(f"Score: {score}\n")]

    if aligned_metadata1 is not None and aligned_metadata2 is not None:
        with open(f'1-{output_filename}', 'w') as file: [file.write(f"{id1} {metadata1}\n") for id1, metadata1 in zip(aligned_identifiers1, aligned_metadata1)]
        with open(f'2-{output_filename}', 'w') as file: [file.write(f"{id2} {metadata2}\n") for id2, metadata2 in zip(aligned_identifiers2, aligned_metadata2)]
    else:
        with open(f'1-{output_filename}', 'w') as file: [file.write(f"{id1}\n") for id1 in aligned_identifiers1]
        with open(f'2-{output_filename}', 'w') as file: [file.write(f"{id2}\n") for id2 in aligned_identifiers2]


def global_alignment_np(sequence1, sequence2, metadata1=None, metadata2=None, gap_penalty=-1, 
                        match_score=1, mismatch_penalty=-10, fasta_name="alignment", threads=None):
    """
    Perform global sequence alignment using dynamic programming (Needleman-Wunsch).

    Parameters:
        sequence1 (str): The first sequence to align.
        sequence2 (str): The second sequence to align.
        gap_penalty (int, optional): Penalty for introducing a gap. Default is -1.
        match_score (int, optional): Score for a match. Default is 1.
        mismatch_penalty (int, optional): Penalty for a mismatch. Default is -1.

    Returns:
        tuple: A tuple containing the aligned longer sequence, aligned shorter sequence, and alignment score.

    Description:
        This function performs global sequence alignment between two input sequences, `sequence1` and `sequence2`,
        using the Needleman-Wunsch algorithm. It aligns the sequences based on the specified scoring parameters
        for gap penalties, match scores, and mismatch penalties.

        The function returns a tuple containing the following elements:
        - The aligned longer sequence (string).
        - The aligned shorter sequence (string).
        - The alignment score (int).

        The aligned sequences are represented as strings where gaps are indicated by '-' characters.

        Additionally, the function saves the alignment as a FASTA file named 'alignment.fasta' and prints a
        human-readable alignment using Biopython's format_alignment function for visualization.
    """
    identifiers1, metadata1 = parse_sequence(sequence1), parse_sequence(metadata1)
    identifiers2, metadata2 = parse_sequence(sequence2), parse_sequence(metadata2)
    m, n = len(identifiers1), len(identifiers2)
    dp_matrix = np.zeros((m + 1, n + 1))

    progress_bar = tqdm.tqdm(total=(m + 1) * (n + 1))
    with ThreadPoolExecutor(threads) as executor:
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if identifiers1[i - 1] == identifiers2[j - 1]:
                    dp_matrix[i][j] = dp_matrix[i - 1][j - 1] + match_score
                else:
                    dp_matrix[i][j] = max(dp_matrix[i - 1][j] + gap_penalty,
                                          dp_matrix[i][j - 1] + gap_penalty,
                                          dp_matrix[i - 1][j - 1] + mismatch_penalty)
                progress_bar.update(1)
    progress_bar.close()

    aligned_identifiers1, aligned_metadata1 = [], []
    aligned_identifiers2, aligned_metadata2 = [], []

    i, j = m, n
    score = dp_matrix[m][n]
    logger.info(f'Calculated score is: {score}')

    while i > 0 and j > 0:
        if identifiers1[i - 1] == identifiers2[j - 1]:
            aligned_identifiers1.append(identifiers1[i - 1])
            aligned_identifiers2.append(identifiers2[j - 1])
            if metadata1 is not None and metadata2 is not None:
                aligned_metadata1.append(metadata1[i - 1])
                aligned_metadata2.append(metadata2[j - 1])
            i -= 1
            j -= 1
        elif dp_matrix[i][j] == dp_matrix[i - 1][j - 1] + mismatch_penalty:
            aligned_identifiers1.append(identifiers1[i - 1])
            aligned_identifiers2.append(identifiers2[j - 1])
            if metadata1 is not None and metadata2 is not None:
                aligned_metadata1.append(metadata1[i - 1])
                aligned_metadata2.append(metadata2[j - 1])
            i -= 1
            j -= 1
        elif dp_matrix[i][j] == dp_matrix[i - 1][j] + gap_penalty:
            aligned_identifiers1.append(identifiers1[i - 1])
            aligned_identifiers2.append('')
            if metadata1 is not None and metadata2 is not None:
                aligned_metadata1.append(metadata1[i - 1])
                aligned_metadata2.append(metadata2[j - 1])
            i -= 1
        else:
            aligned_identifiers1.append('')
            aligned_identifiers2.append(identifiers2[j - 1])
            if metadata1 is not None and metadata2 is not None:
                aligned_metadata1.append(metadata1[i - 1])
                aligned_metadata2.append(metadata2[j - 1])
            j -= 1

    aligned_identifiers1.reverse()
    aligned_identifiers2.reverse()
    if metadata1 is not None and metadata2 is not None:
        aligned_metadata1.reverse()
        aligned_metadata2.reverse()

    padded_sequences1, padded_sequences2 = [], []

    for seq1, seq2 in zip(aligned_identifiers1, aligned_identifiers2):
        if seq1 == '':
            padded_seq1 = '-' * len(seq2)
            padded_sequences1.append(padded_seq1)
            padded_sequences2.append(seq2)
        elif seq2 == '':
            padded_seq2 = '-' * len(seq1)
            padded_sequences1.append(seq1)
            padded_sequences2.append(padded_seq2)
        else:
            if len(seq1) < len(seq2):
                padded_seq1 = seq1 + '-' * (len(seq2) - len(seq1))
                padded_sequences1.append(padded_seq1)
                padded_sequences2.append(seq2)
            else:
                padded_seq2 = seq2 + '-' * (len(seq1) - len(seq2))
                padded_sequences1.append(seq1)
                padded_sequences2.append(padded_seq2)

    if metadata1 is not None and metadata2 is not None:
        write_stockholm_alignment_with_metadata(padded_sequences1, padded_sequences2, aligned_metadata1, 
                                                aligned_metadata2, score, f'{fasta_name}.sto')
        write_text_format(padded_sequences1, padded_sequences2, score, f'{fasta_name}-text.txt', 
                            aligned_metadata1, aligned_metadata2)
    else:
        write_text_format(padded_sequences1, padded_sequences2, score, f'{fasta_name}-text.txt')

    record1 = SeqRecord(Seq("|".join(padded_sequences1)), id="sequence1")
    record2 = SeqRecord(Seq("|".join(padded_sequences2)), id="sequence2")

    SeqIO.write([record1, record2], f'{fasta_name}.fasta', "fasta")

    return '|'.join(aligned_identifiers1), '|'.join(aligned_identifiers2), score
