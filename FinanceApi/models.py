from django.db import models


class OrderBook(models.Model):
    id = models.AutoField(primary_key=True)
    low_24h = models.FloatField()
    high_24h = models.FloatField()
    avg_24h = models.FloatField()
    volume_24h = models.FloatField()
    day = models.TextField()
    week = models.TextField()
    mount = models.TextField()

    def to_json(self):
        return {"id": self.id,
                "low_24h": self.low_24h,
                "high_24h": self.high_24h,
                "avg_24h": self.avg_24h,
                "volume_24h": self.volume_24h,
                "day": self.day,
                "week": self.week,
                "mount": self.mount
                }


# class Daily(models.Model):
#     daily_low = models.TextField()
#     daily_high = models.TextField()
#     daily_avg = models.TextField()
#     daily_volume = models.TextField()
#     day = models.TextField

#     def to_json(self):
#         return {
#             "daily_low": self.daily_low,
#             "daily_high": self.daily_high,
#             "daily_avg": self.daily_avg,
#             "daily_volume": self.daily_volume,
#             "day": self.day
#         }
