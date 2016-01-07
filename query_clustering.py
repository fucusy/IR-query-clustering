#!/usr/bin/python

import logging
import sys
import pickle
import operator
from helper.helper import UF
import config.config as config
import datetime

class BipartiteCluster:
    data_path = ''

    query_to_int = {}
    int_to_query = []
    docid_to_int = {}
    int_to_docid = []

    query_uf = UF()
    docid_uf = UF()

    docid_id_to_query_id_list = {}
    query_id_to_docid_id_list = {}

    def __init__(self, data_path):
        # todo check data format
        # todo add data format description
        self.data_path = data_path

    def index(self):
        for line in open(self.data_path):
            split_line = line.split('\t')
            query = ''
            docid = ''
            try:
                query = split_line[1].strip()
                docid = split_line[0].strip()
            except:
                logging.warning('can not get query and docid from line:%s' % line)
            if query == '' or docid == '':
                continue

            if query in self.query_to_int.keys():
                query_int = self.query_to_int[query]
            else:
                self.int_to_query.append(query)
                query_int = len(self.int_to_query) - 1
                self.query_to_int[query] = query_int


            if docid in self.docid_to_int.keys():
                docid_id = self.docid_to_int[docid]
            else:
                self.int_to_docid.append(docid)
                docid_id = len(self.int_to_docid) - 1
                self.docid_to_int[docid] = docid_id

            if docid_id in self.docid_id_to_query_id_list.keys():
                self.docid_id_to_query_id_list[docid_id].add(query_int)
            else:
                self.docid_id_to_query_id_list[docid_id] = set([query_int])

            if query_int in self.query_id_to_docid_id_list.keys():
                self.query_id_to_docid_id_list[query_int].add(docid_id)
            else:
                self.query_id_to_docid_id_list[query_int] = set([docid_id])
            logging.debug('processing line: %s' % line)

    def get_similarity_list(self, is_query=True):
        pair_holder = {}
        if is_query:
            list_value = self.docid_id_to_query_id_list.values()
        else:
            list_value = self.query_id_to_docid_id_list.values()

        for k_list in list_value:
            k_list = list(k_list)
            for i in range(len(k_list)):
                for j in range(i + 1, len(k_list)):
                    if k_list[i] < k_list[j]:
                        keyword = "%s-%s" % (k_list[i], k_list[j])
                    else:
                        keyword = "%s-%s" % (k_list[j], k_list[i])
                    pair_holder[keyword] = 0

        for pair in pair_holder.keys():
            split_pair = pair.split('-')
            try:
                id1 = int(split_pair[0])
                id2 = int(split_pair[1])
            except Exception, e:
                logging.warning('fail to extract info from pair_key: %s' % pair)
                logging.warning('error msg: %s', e)
                continue
            if id1 == id2:
                continue
            if is_query:
                id1_edge_set = self.query_id_to_docid_id_list[id1]
                id2_edge_set = self.query_id_to_docid_id_list[id2]
            else:
                id1_edge_set = self.docid_id_to_query_id_list[id1]
                id2_edge_set = self.docid_id_to_query_id_list[id2]
            intersect = id1_edge_set & id2_edge_set
            union = id1_edge_set | id2_edge_set
            if len(union) == 0:
                similarity = 0
            else:
                similarity = len(intersect) * 1.0 / len(union)
            pair_holder[pair] = similarity
        sorted_pair_holder = sorted(pair_holder.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_pair_holder

    def del_index(self, index_id, is_query = True):
        if is_query:
            logging.debug('delete query_id: %s', index_id)
        else:
            logging.debug('delete docid_id: %s', index_id)
        if is_query:
            try:
                for docid_id in self.query_id_to_docid_id_list[index_id]:
                    try:
                        self.docid_id_to_query_id_list[docid_id].remove(index_id)
                    except:
                        pass
            except:
                pass

            try:
                del self.query_id_to_docid_id_list[index_id]
            except:
                pass
        else:
            try:
                for query_id in self.docid_id_to_query_id_list[index_id]:
                    try:
                        self.query_id_to_docid_id_list[query_id].remove(index_id)
                    except:
                        pass
            except:
                pass

            try:
                del self.docid_id_to_query_id_list[index_id]
            except:
                pass




    def cluster(self, max_iteration=3000):
        self.index()
        self.query_uf.init(len(self.int_to_query))
        self.docid_uf.init(len(self.int_to_docid))

        is_query = True
        similarity_list = self.get_similarity_list(is_query)
        out_put_count = 0
        iteration_count = 0

        while len(similarity_list) > 0:
            for pair, similarity in similarity_list:
                if similarity < 0.8:
                    break
                out_put_count += 1
                split_pair = pair.split('-')
                try:
                    id1 = int(split_pair[0])
                    id2 = int(split_pair[1])
                except Exception, e:
                    logging.warning("fail to extract info from %s" % split_pair)
                    logging.warning("error msg: %s" % e)
                if is_query:
                    logging.debug("%s|%s %s|%s, similarity: %0.8f" % (id1, self.int_to_query[id1], id2, self.int_to_query[id2], similarity))
                else:
                    logging.debug("%s|%s %s|%s, similarity: %0.8f" % (id1, self.int_to_docid[id1], id2, self.int_to_docid[id2], similarity))
                if is_query:
                    self.query_uf.union(id1, id2)
                    parent = self.query_uf.get_parent(id1)
                else:
                    self.docid_uf.union(id1, id2)
                    parent = self.docid_uf.get_parent(id1)

                if id1 != parent:
                    self.del_index(id1, is_query)
                if id2 != parent:
                    self.del_index(id2, is_query)

            is_query = not is_query
            similarity_list = self.get_similarity_list(is_query)
            iteration_count += 1
            if iteration_count > max_iteration:
                break

        doc_cluster_to_docid_dic = {}
        query_cluster_to_query_dic = {}
        for i in range(len(self.int_to_query)):
            parent = self.query_uf.get_parent(i)
            if parent in query_cluster_to_query_dic:
                query_cluster_to_query_dic[parent].append(self.int_to_query[i])
            else:
                query_cluster_to_query_dic[parent] = [self.int_to_query[i]]

        self.docid_uf.init(len(self.int_to_docid))
        for i in range(len(self.int_to_docid)):
            parent = self.docid_uf.get_parent(i)
            if parent in doc_cluster_to_docid_dic:
                doc_cluster_to_docid_dic[parent].append(self.int_to_docid[i])
            else:
                doc_cluster_to_docid_dic[parent] = [self.int_to_docid[i]]

        # for cluster in doc_cluster_to_docid_dic.keys():
        #     if len(doc_cluster_to_docid_dic[cluster]) > 1:
        #         logging.info("%s: %s" % (cluster, ','.join(doc_cluster_to_docid_dic[cluster])))

        for cluster in query_cluster_to_query_dic.keys():
            if len(query_cluster_to_query_dic[cluster]) > 1:
                logging.info("%s: %s" % (cluster, ','.join(query_cluster_to_query_dic[cluster])))


if __name__ == '__main__':
    LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}

    start_time = datetime.datetime.now()
    level = logging.INFO
    if len(sys.argv) >= 2:
        level_name = sys.argv[1]
        level = LEVELS.get(level_name, logging.NOTSET)

    FORMAT = '%(asctime)-12s[%(levelname)s] %(message)s'
    logging.basicConfig(level=level, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S', filename='query_clustering.log')
    logging.info('start program---------------------')
    c = BipartiteCluster(config.data_path)
    c.cluster()

    end_time = datetime.datetime.now()
    logging.info('total running time: %.2f second' % (end_time - start_time).seconds)
    logging.info('end program---------------------')