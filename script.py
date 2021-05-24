import argparse
from db_service import DBService
from outer_format import JSONDump, XMLDump
from queries import *

MYSQL_SETTINGS = {
    'host': 'localhost',
    'username': 'root',
    'password': 'toor',
    'database': 'database'
}


def arg_parser():
    parser = argparse.ArgumentParser(description='With this script, you can combine two files into a file of the '
                                                 'desired format')
    parser.add_argument('students_file_path', type=str, help='Provide a path to students file')
    parser.add_argument('rooms_file_path', type=str, help='Provide a path to rooms file')
    parser.add_argument('outer_format', type=str, help='Choose an outer format', choices=['xml', 'json'])

    return parser


def main(students_path, rooms_path, file_format):
    db = DBService(MYSQL_SETTINGS)
    db.connect_or_create()

    db.init_table(QUERY_INITIAL)
    db.fullfill(students_path, "students")
    db.fullfill(rooms_path, "rooms")

    query_list = [QUERY_1, QUERY_2, QUERY_3, QUERY_4]
    query_num = 1
    for query in query_list:

        result = db.execute_query(query)

        if file_format == 'json':
            with open(f'outer_format_files/json/rooms_sorted_query{query_num}.json', 'tw+', encoding='UTF-8') as file:
                query_num += 1
                JSONDumper = JSONDump()
                file.write(JSONDumper.dump(result))

        elif file_format == "xml":
            with open(f'outer_format_files/xml/rooms_sorted_query{query_num}.xml', 'tw+', encoding='UTF-8') as file:
                query_num += 1
                XMLDumper = XMLDump()
                file.write(XMLDumper.dump(result))

    db.update_query(QUERY_FOR_INDEX)
    db.close_connection()


if __name__ == '__main__':
    args = arg_parser().parse_args()
    main(args.students_file_path, args.rooms_file_path, args.outer_format)
