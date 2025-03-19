from rest_framework import serializers
from .models import Grade


class GradeSerializer(serializers.ModelSerializer):
    computed_score = serializers.SerializerMethodField()

    class Meta:
        model = Grade
        fields = [
            'student',
            'course',
            'final_exam',
            'assignments',
            'regular_quiz',
            'attendance',
            'gpa',
            'computed_score'
        ]

    # 通过查询参数传入权重，计算加权成绩
    def get_computed_score(self, obj):
        request = self.context.get('request')
        # 默认权重设置（可根据需求调整）
        weight_final = 0.4
        weight_assignments = 0.4
        weight_regular_quiz = 0.1
        weight_attendance = 0.1

        if request:
            try:
                weight_final = float(request.query_params.get('weight_final', weight_final))
                weight_assignments = float(request.query_params.get('weight_assignments', weight_assignments))
                weight_regular_quiz = float(request.query_params.get('weight_regular_quiz', weight_regular_quiz))
                weight_attendance = float(request.query_params.get('weight_attendance', weight_attendance))
            except ValueError:
                # 如果转换失败，则继续使用默认值
                pass

        computed = (
                obj.final_exam * weight_final +
                obj.assignments * weight_assignments +
                obj.regular_quiz * weight_regular_quiz +
                obj.attendance * weight_attendance
        )
        return round(computed, 2)

    # 分别校验各个分数字段，确保它们在0-100的合理范围内
    def validate_final_exam(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Final exam score must be between 0 and 100.")
        return value

    def validate_assignments(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Assignment score must be between 0 and 100.")
        return value

    def validate_regular_quiz(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Regular quiz score must be between 0 and 100.")
        return value

    def validate_attendance(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Attendance percentage must be between 0 and 100.")
        return value

    # GPA 的范围校验（假设 GPA 范围为0-4；如果有其他要求，请调整）
    def validate_gpa(self, value):
        if value < 0 or value > 4:
            raise serializers.ValidationError("GPA must be between 0 and 4.")
        return value

    def validate(self, data):
        # 可以添加跨字段校验，比如确保某些字段组合符合业务逻辑
        return data

