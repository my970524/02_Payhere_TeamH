from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import AccountBook, AccountBookRecord


class AccountBooksRecordModelSerializer(ModelSerializer):
    """
    Assignee : 상백

    참조 및 역참조를 통해 AccountBookRecord 모델 객체들의 금액을 for문을 이용하여
    AccountBookRecord 모델 데이터가 생성된 시점까지의 잔액을 계산
    """

    balance = serializers.SerializerMethodField()

    def get_balance(self, obj):
        balance = obj.account_book.balance
        for record in obj.account_book.account_book_record.all().filter(is_deleted=False):
            if obj.id >= record.id:
                balance += record.amount
        return balance

    class Meta:
        model = AccountBookRecord
        fields = ("amount", "memo", "balance", "created_at")


class AccountBooksModelSerializer(ModelSerializer):
    """
    Assignee : 상백

    View단에서 AccountBook 모델의 객체가 주어졌을 때,
    역참조를 통해 AccountBookRecord 모델의 쿼리셋을 가져오기

    AccountBookRecord 모델 쿼리셋에서 for문을 이용해
    현재까지의 잔액을 계산하는 로직 구성

    내부에 정의된 create 메소드 override로 로그인된 user로 AccountBook 모델 생성
    """

    가계부_고유번호 = serializers.IntegerField(source="id", required=False, read_only=True)
    total_balance = serializers.SerializerMethodField(required=False, read_only=True)
    accountbook_record = serializers.SerializerMethodField(required=False, read_only=True)

    def get_total_balance(self, obj):
        accountbookrecords = obj.account_book_record.all().filter(is_deleted=False)
        total_balance = obj.balance
        for record in accountbookrecords:
            total_balance += record.amount
        return total_balance

    def get_accountbook_record(self, obj):
        accountbook_records = obj.account_book_record.all().filter(is_deleted=False)
        accountbook_records_serializer = AccountBooksRecordModelSerializer(accountbook_records, many=True)
        return accountbook_records_serializer.data

    def create(self, validated_data):
        user = self.context["user"]
        accountbook = AccountBook(user=user, **validated_data)
        accountbook.save()
        return accountbook

    class Meta:
        model = AccountBook
        fields = ("user", "title", "balance", "가계부_고유번호", "total_balance", "accountbook_record")
        read_only_fields = ["user"]