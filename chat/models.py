#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from app import BaseModel
import peewee as pw
from datetime import datetime
from user.models import User
from enum import Enum,unique
#��� unique װ����
@unique
class Msg_type(Enum):
    #��Ϣ���� 0-�ı����� 1-ͼƬ���� 2-ϵͳ֪ͨ����
    Text = 0
    Image = 1
    Notice=2
    


class Room(BaseModel):
    """
    ��������
    �̳���BaseModel��ֱ�ӹ���db������Ҳ�̳���Model Model���ṩ��ɾ��ĵĺ���
    """
    room_id = pw.IntegerField(primary_key=True)  # ����������ʽ����Ļ�peeweeĬ�϶���һ��������id
    receiver_id = pw.ForeignKeyField(User, verbose_name="�����ߵ�ѧ��")
    sender_id = pw.ForeignKeyField(User, verbose_name="���ͷ���ѧ��")
    #�÷�������ڷ����ߣ��Ǹ÷������ڶ෿���е�һ��(room_id���п���)
    



class Message(BaseModel):
    """
    �����¼��
    ��¼ĳ�������ڷ�������������(���ͺͽ���)���뷿��һ���������ڷ�����
    �̳���BaseModel��ֱ�ӹ���db������Ҳ�̳���Model Model���ṩ��ɾ��ĵĺ���
    """
    msg_id = pw.IntegerField(primary_key=True,verbose_name="��Ϣ���")
    msg_time = pw.DateField(verbose_name="����ʱ��",
                                null=False,
                                default=datetime.utcnow())
    
    room_id = pw.ForeignKeyField(Room,verbose_name="�����")  
    sender_id = pw.ForeignKeyField(User, verbose_name="���ͷ���ѧ��")

    #��Ϣ���� 0-�ı����� 1-ͼƬ���� 2-ϵͳ֪ͨ����
    msg_type = pw.IntegerField(verbose="��Ϣ����", null=False, default=Msg_type.Text.value,
                                constraints=[pw.Check("state >=0")])
    
    #��Ϣ���ݣ����ۺ������ͣ����ݶ�ֻ��string��ʽ����
    msg = pw.CharField(verbose_name="��Ϣ����", max_length=1024)
    
    #����Ƿ�ɼ���1�ɼ�0���ɼ���Ĭ��1 
    visible = pw.IntegerField(verbose_name="�Ƿ���ʾ", null=False, default=1)


class Recent_Chat_List(BaseModel):
    """
    ������Ϣ��
    �̳���BaseModel��ֱ�ӹ���db������Ҳ�̳���Model Model���ṩ��ɾ��ĵĺ���
    """
    receiver_id = pw.ForeignKeyField(User,primary_key=True, verbose_name="�����ߵ�ѧ��")
    #����������������
    
    last_time = pw.DateField(verbose_name="������ʱ��")
    
    unread = pw.IntegerField(verbose_name="δ������", null=False, default=0)