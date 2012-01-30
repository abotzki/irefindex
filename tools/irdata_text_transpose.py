#!/usr/bin/env python

"""
Transpose input lines, writing fields from each line to separate output lines.

The input tokens are read from a file or stream (depending on the arguments)
employing a tab-separated format (or a format employing a specified delimiter)
where the input tokens are (unless otherwise stated) the only fields on each
line:

<field>...

The output will resemble the following:

<field>
...

Where a start field is specified, preceding fields will not be transposed and
will appear together on every output line derived from a particular input line.

Thus, the input data will resemble the following:

<preceding-field>... <field>...

The corresponding output will resemble this:

<preceding-field>... <field>
<preceding-field>... ...
"""

from irdata.data import RawImportFileReader, RawImportFile, reread, rewrite, \
    index_for_int, int_or_none, partition
import irdata.cmd
import sys, cmdsyntax

syntax_description = """
    --help |
    [ -f <start-field> ]
    [ -t <end-field> ]
    [ -d <delimiter> ]
    [ -w <delimiter-within-fields> ]
    [ -s <sequence-start> ]
    ( <filename> | - )
    """

# Main program.

def main():

    # Get the command line options.

    syntax = cmdsyntax.Syntax(syntax_description)
    try:
        matches = syntax.get_args(sys.argv[1:])
        args = matches[0]
    except IndexError:
        print >>sys.stderr, "Syntax:"
        print >>sys.stderr, syntax_description
        sys.exit(1)
    else:
        if args.has_key("help"):
            print >>sys.stderr, __doc__
            print >>sys.stderr, "Syntax:"
            print >>sys.stderr, syntax_description
            sys.exit(1)

    start_field = index_for_int(args.get("start-field", 1))
    end_field = int_or_none(args.get("end-field", None)) # treat 1-index as 0-index plus one

    delimiter = args.get("delimiter", "\t")
    delimiter_within_fields = args.get("delimiter-within-fields", "\t")

    sequence_start = int_or_none(args.get("sequence-start"))

    if args.has_key("filename"):
        filename_or_stream = args["filename"]
    else:
        filename_or_stream = reread(sys.stdin)

    reader = RawImportFileReader(filename_or_stream, delimiter=delimiter)
    writer = RawImportFile(rewrite(sys.stdout))

    try:
        try:
            for details in reader:

                # Process the data.

                preceding, fields, following = partition(details, start_field, end_field)

                if delimiter_within_fields != delimiter:
                    split_fields = []
                    for field in fields:
                        split_fields += field.split(delimiter_within_fields)
                    fields = split_fields

                for i, field in enumerate(fields):
                    if sequence_start is not None:
                        values = [i + sequence_start, field]
                    else:
                        values = [field]
                    writer.append(preceding + values + following)

        except IOError, exc:
            print >>sys.stderr, "%s: %s" % (irdata.cmd.get_progname(), exc)

    finally:
        writer.close()
        reader.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)

# vim: tabstop=4 expandtab shiftwidth=4
