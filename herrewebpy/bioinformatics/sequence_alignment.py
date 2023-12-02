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

def write_stockholm_alignment_with_metadata(aligned_identifiers1, aligned_identifiers2, aligned_metadata1, aligned_metadata2, score, output_filename):
    """
    Write a multiple sequence alignment with associated metadata in Stockholm format to a file.

    Parameters:
    - aligned_identifiers1 (list): List of identifiers for the first aligned sequence.
    - aligned_identifiers2 (list): List of identifiers for the second aligned sequence.
    - aligned_metadata1 (list): List of metadata annotations for the first aligned sequence.
    - aligned_metadata2 (list): List of metadata annotations for the second aligned sequence.
    - score (float): Alignment score to be included as a global feature.
    - output_filename (str): Name of the file to write the Stockholm-formatted alignment.

    The function opens the specified file in write mode, writes the Stockholm header,
    and iterates over aligned sequences and their associated metadata, writing them to the file.
    The alignment score is also included as a global feature. The file is closed automatically
    upon exiting the function.

    Example:
    >>> aligned_identifiers1 = ['A', 'B', 'C']
    >>> aligned_identifiers2 = ['X', 'Y', 'Z']
    >>> aligned_metadata1 = ['metaA', 'metaB', 'metaC']
    >>> aligned_metadata2 = ['metaX', 'metaY', 'metaZ']
    >>> score = 42.0
    >>> write_stockholm_alignment_with_metadata(aligned_identifiers1, aligned_identifiers2,
    ...                                          aligned_metadata1, aligned_metadata2, score, 'output.sto')
    """
    with open(output_filename, 'w') as stockholm_file:
        stockholm_file.write("# STOCKHOLM 1.0\n")
        for id1, id2, metadata1, metadata2 in zip(aligned_identifiers1, aligned_identifiers2, aligned_metadata1, aligned_metadata2):
            stockholm_file.write(f"{id1}\n")
            stockholm_file.write(f"{id2}\n")
            stockholm_file.write(f"#=GC METADATA1 {metadata1}\n")
            stockholm_file.write(f"#=GC METADATA2 {metadata2}\n")
        stockholm_file.write(f"#=GF SCORE: {score}\n")
    stockholm_file.close()


def write_clustal_alignment(sequences, output_filename):
    """
    Write to clustal format
    """
    with open(output_filename, 'w') as clustal_file:
        for sequence in sequences:
            clustal_file.write(f"{sequence.id.ljust(20)} {sequence.seq}\n")


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


class SequenceAlignment:
    def __init__(self, sequence1, sequence2, metadata1=None, metadata2=None, gap_penalty=-2,
                 match_score=1, mismatch_penalty=-1, filename="alignment", threads=None,
                 stockholm=True, fasta=True, clustal=False, padding='-'):
        """
        Perform global sequence alignment and save the results in various formats.

        Parameters:
            sequence1 (str): The first sequence to align.
            sequence2 (str): The second sequence to align.
            metadata1 (str, optional): Metadata for the first sequence. Default is None.
            metadata2 (str, optional): Metadata for the second sequence. Default is None.
            gap_penalty (int, optional): Penalty for introducing a gap. Default is -1.
            match_score (int, optional): Score for a match. Default is 1.
            mismatch_penalty (int, optional): Penalty for a mismatch. Default is -10.
            filename (str, optional): Name for the output files. Default is "alignment".
            threads (int, optional): Number of threads for parallel execution. Default is None.
            stockholm (bool, optional): Whether to output in Stockholm format. Default is True.
            fasta (bool, optional): Whether to output in FASTA format. Default is True.
            clustal (bool, optional): Whether to output in Clustal format. Default is False.
            padding (str, optional): Padding character for alignment. Default is '-'.

        Returns:
            int: The alignment score.
        """
        self.sequence1 = sequence1
        self.sequence2 = sequence2
        self.metadata1 = metadata1
        self.metadata2 = metadata2
        self.gap_penalty = gap_penalty
        self.match_score = match_score
        self.mismatch_penalty = mismatch_penalty
        self.filename = filename
        self.threads = threads
        self.stockholm = stockholm
        self.fasta = fasta
        self.clustal = clustal
        self.padding = padding

        self.align()


    def align(self):
        padded_sequences1, padded_sequences2, aligned_metadata1, aligned_metadata2, score = self._global_alignment_np(
            self.sequence1, self.sequence2, self.metadata1, self.metadata2,
            self.gap_penalty, self.match_score, self.mismatch_penalty, self.threads, self.padding
        )

        if self.metadata1 is not None and self.metadata2 is not None:
            if self.stockholm:
                write_stockholm_alignment_with_metadata(
                    padded_sequences1, padded_sequences2, aligned_metadata1, aligned_metadata2, score, f'{self.filename}.sto'
                )
            if self.fasta:
                write_text_format(padded_sequences1, padded_sequences2, score, f'{self.filename}-text.txt',
                                  aligned_metadata1, aligned_metadata2)
        else:
            write_text_format(padded_sequences1, padded_sequences2, score, f'{self.filename}-text.txt')

        record1 = SeqRecord(Seq("|".join(padded_sequences1)), id="sequence1")
        record2 = SeqRecord(Seq("|".join(padded_sequences2)), id="sequence2")

        if self.fasta:
            SeqIO.write([record1, record2], f'{self.filename}.fasta', "fasta")

        if self.clustal:
            sequences = [SeqRecord(Seq("|".join(padded_sequences1)), id="sequence1"),
                         SeqRecord(Seq("|".join(padded_sequences2)), id="sequence2")]
            write_clustal_alignment(sequences, f'{self.filename}.aln')

        self.score = score


    def _parse_sequence(self, sequence):
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
        elif isinstance(sequence, list):
            sequence = '|'.join(sequence)
        logger.info(f'Assuming type is string, returning list')
        identifiers = [item.strip('|') for item in sequence.split('|') if item.strip('|')]
        return identifiers


    def _pad_sequences(self, aligned_identifiers1, aligned_identifiers2, padding):
            """
            Add paddings (-) to sequences. Drastically helps visualize alignments.
            """
            padded_sequences1, padded_sequences2 = [], []
            for seq1, seq2 in zip(aligned_identifiers1, aligned_identifiers2):
                if seq1 == '':
                    padded_seq1 = f'{padding}' * len(seq2)
                    padded_sequences1.append(padded_seq1)
                    padded_sequences2.append(seq2)
                elif seq2 == '':
                    padded_seq2 = f'{padding}' * len(seq1)
                    padded_sequences1.append(seq1)
                    padded_sequences2.append(padded_seq2)
                else:
                    if len(seq1) < len(seq2):
                        padded_seq1 = seq1 + f'{padding}' * (len(seq2) - len(seq1))
                        padded_sequences1.append(padded_seq1)
                        padded_sequences2.append(seq2)
                    else:
                        padded_seq2 = seq2 + f'{padding}' * (len(seq1) - len(seq2))
                        padded_sequences1.append(seq1)
                        padded_sequences2.append(padded_seq2)
            return padded_sequences1, padded_sequences2


    def _global_alignment_np(self, sequence1, sequence2, metadata1, metadata2, gap_penalty, 
                            match_score, mismatch_penalty, threads, padding):
        """
        Description:
            This function performs global sequence alignment between two input sequences, `sequence1` and `sequence2`,
            using the Needleman-Wunsch algorithm. It aligns the sequences based on the specified scoring parameters
            for gap penalties, match scores, and mismatch penalties.

            The function returns a tuple containing the following elements:
            - The aligned longer sequence (list of strings) where gaps are indicated by '-' characters.
            - The aligned shorter sequence (list of strings) where gaps are indicated by '-' characters.
            - Aligned metadata for sequence1 (list of strings).
            - Aligned metadata for sequence2 (list of strings).
            - The alignment score (int).

        Note:
            If additional metadata is not provided (metadata1 or metadata2 is None), the corresponding aligned_metadata
            lists will also be None.

        Example:
            ```python
            sequence1 = "AGCT"
            sequence2 = "AAGCT"
            aligned_seq1, aligned_seq2, align_metadata1, align_metadata2, score = _global_alignment_np(
                sequence1, sequence2, metadata1="ABC", metadata2="XYZ"
            )
            ```

        """
        identifiers1, metadata1 = self._parse_sequence(sequence1), self._parse_sequence(metadata1)
        identifiers2, metadata2 = self._parse_sequence(sequence2), self._parse_sequence(metadata2)
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

        score = dp_matrix[m][n]
        logger.info(f'Calculated score is: {score}. (negative is generally bad, positive is good)')
        match_count, mismatch_count, gap_count = 0, 0, 0

        # Finds matches/mismatches and introduces gaps if mismatches are found
        while m > 0 and n > 0:
            if identifiers1[m - 1] == identifiers2[n - 1]:
                aligned_identifiers1.append(identifiers1[m - 1]), aligned_identifiers2.append(identifiers2[n - 1])
                if metadata1 is not None and metadata2 is not None:
                    aligned_metadata1.append(metadata1[m - 1]), aligned_metadata2.append(metadata2[n - 1])
                m -= 1
                n -= 1
                match_count += 1
            elif dp_matrix[m][n] == dp_matrix[m - 1][n - 1] + mismatch_penalty:
                aligned_identifiers1.append(identifiers1[m - 1]), aligned_identifiers2.append(identifiers2[n - 1])
                if metadata1 is not None and metadata2 is not None:
                    aligned_metadata1.append(metadata1[m - 1]), aligned_metadata2.append(metadata2[n - 1])
                m -= 1
                n -= 1
                mismatch_count += 1
            elif dp_matrix[m][n] == dp_matrix[m - 1][n] + gap_penalty:
                aligned_identifiers1.append(identifiers1[m - 1]), aligned_identifiers2.append('')
                if metadata1 is not None and metadata2 is not None:
                    aligned_metadata1.append(metadata1[m - 1]),aligned_metadata2.append(metadata2[n - 1])
                m -= 1
                gap_count += 1
            else:
                aligned_identifiers1.append(''), aligned_identifiers2.append(identifiers2[n - 1])
                if metadata1 is not None and metadata2 is not None:
                    aligned_metadata1.append(metadata1[m - 1]), aligned_metadata2.append(metadata2[n - 1])
                n -= 1
        
        logger.info(f'{mismatch_count} mismatches found and {gap_count} gaps found. {match_count} matches found.')

        aligned_identifiers1.reverse(), aligned_identifiers2.reverse()
        if metadata1 is not None and metadata2 is not None:
            aligned_metadata1.reverse(), aligned_metadata2.reverse()

        padded_sequences1, padded_sequences2 =self._pad_sequences(aligned_identifiers1, aligned_identifiers2, padding)
        
        return padded_sequences1, padded_sequences2, aligned_metadata1, aligned_metadata2, score
