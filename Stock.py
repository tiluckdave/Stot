import discord
import random
import requests
import Util
from discord.ext import commands
from bselib.bse import BSE


class Stock(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='search',
        aliases=['find', 'look', 's'],
        help="Search the company related to provided search term"
    )
    async def search(self, ctx, term=None):
        b = BSE()
        msg = await ctx.send(embed=Util.loading_embed)
        searchEmbed = discord.Embed(title=f"Your Search '{term}'",
                                    description=f"List of all Stocks based on your search.\nUse `{self.client.command_prefix[0]}quote <script-code>` to view all details of respective company.\nSource: [bseindia.com](https://www.bseindia.com/)",
                                    colour=random.randint(0, 0xffffff)
                                    )
        stocks = b.script(term)
        if stocks:
            for key in stocks:
                searchEmbed.add_field(
                    name=f"{stocks[key]}", value=f"Script Code: **{key}**", inline=False)
        else:
            searchEmbed.add_field(
                name="No Stocks Found", value="Are you sure the company is listed under Bombay Stock Exchange?", inline=False)
        searchEmbed.set_author(name="{}".format(
            ctx.message.author), icon_url=ctx.message.author.avatar_url)
        await msg.edit(embed=searchEmbed)

    @commands.command(name='quote', aliases=['estimate', 'q'], help="Returns a detailed quote of provided company id.")
    async def quote(self, ctx, cid=None):
        msg = await ctx.send(embed=Util.loading_embed)
        b = BSE()
        data = b.quote(cid)
        QuoteEmbed = discord.Embed(
            title=f"{data['stockName']}\n", description=f"Get a complete chart view. **[Click here.](https://in.tradingview.com/chart/?symbol=BSE%3A{data['securityId']})**\nSource: [bseindia.com](https://www.bseindia.com/)", colour=random.randint(0, 0xffffff))
        QuoteEmbed.add_field(name=f"Current Price: **{data['stockPrice']}**",
                             value=f"Day's Change: **{data['change']}**\nChange Percent: **({data['pChange']}%)**\n", inline=False)
        QuoteEmbed.add_field(
            name=f"Details", value=f"Last Open: **{data['lastOpen']}**\nPrevious Close: **{data['previousClose']}**\n", inline=False)
        QuoteEmbed.add_field(
            name=f"Statistics", value=f"Day's High: **{data['daysHigh']}**\nDay's Low: **{data['daysLow']}**\n52 Week High: **{data['fiftytwo_WeekHigh']}**\n52 Week Low: **{data['fiftytwo_WeekLow']}**\n", inline=False)
        QuoteEmbed.add_field(name=f"Valuation Measures",
                             value=f"Market Cap: **{data['mktCap']['value']} {data['mktCap']['in']}**\nTotal Traded Quantity: **{data['totalTradedQty']['value']} {data['totalTradedQty']['in']}**\nTotal Traded Value: **{data['totalTradedValue']['value']} {data['totalTradedValue']['in']}**\n", inline=False)
        QuoteEmbed.set_author(name="{}".format(
            ctx.message.author), icon_url=ctx.message.author.avatar_url)
        await msg.edit(embed=QuoteEmbed)

    @commands.command(name='top_gainers', aliases=['gainers', 'topg', 'tg'], help="Returns day's top gainers")
    async def top_gainers(self, ctx):
        msg = await ctx.send(embed=Util.loading_embed)
        b = BSE()
        data = b.get_gainers()
        QuoteEmbed = discord.Embed(
            title=f"Day's Top Gainers", description=f"below are today's top performers of BSE\nSource: [bseindia.com](https://www.bseindia.com/)", colour=random.randint(0, 0xffffff))
        rank = 1
        for i in data['gainers']:
            cs = b.quote(i['scriptCode'])
            QuoteEmbed.add_field(
                name=f"#{rank}. {str(cs['stockName'])}", value=f"[Complete chart here.](https://in.tradingview.com/chart/?symbol=BSE%3A{i['securityID']})\nLast Traded Price: **{i['LTP']}**\nDay's Change: **+{i['change']}** **(+{i['pChange']}%)**\n", inline=False)
            rank += 1
        QuoteEmbed.set_author(name="{}".format(
            ctx.message.author), icon_url=ctx.message.author.avatar_url)
        await msg.edit(embed=QuoteEmbed)

    @commands.command(name='top_losers', aliases=['losers', 'topl', 'tl'], help="Returns day's top gainers")
    async def top_losers(self, ctx):
        msg = await ctx.send(embed=Util.loading_embed)
        b = BSE()
        data = b.get_losers()
        QuoteEmbed = discord.Embed(
            title=f"Day's Top Losers", description=f"below are today's worst performers of BSE\nSource: [bseindia.com](https://www.bseindia.com/)", colour=random.randint(0, 0xffffff))
        rank = 1
        for i in data['losers']:
            cs = b.quote(i['scriptCode'])
            QuoteEmbed.add_field(
                name=f"#{rank}. {cs['stockName']}", value=f"[Complete chart here.](https://in.tradingview.com/chart/?symbol=BSE%3A{i['securityID']})\nLast Traded Price: **{i['LTP']}**\nDay's Change: **{i['change']}** **({i['pChange']}%)**\n", inline=False)
            rank += 1
        QuoteEmbed.set_author(name="{}".format(
            ctx.message.author), icon_url=ctx.message.author.avatar_url)
        await msg.edit(embed=QuoteEmbed)

    @commands.command(name='news', aliases=['n'], help="Returns latest news related to provided stock script Id")
    async def news(self, ctx, cid=None):
        msg = await ctx.send(embed=Util.loading_embed)
        b = BSE()
        data = b.news(cid)
        cs = b.quote(cid)
        QuoteEmbed = discord.Embed(
            title=f"Latest News for {cs['stockName']}", description="Source: [bseindia.com](https://www.bseindia.com/)", colour=random.randint(0, 0xffffff))
        srno = 1
        for i in data['news']:
            QuoteEmbed.add_field(
                name=f"{srno} - {i['title']}", value=f"{i['publisheddate']} ・ [Know More]({i['link']})", inline=False)
            srno += 1
        QuoteEmbed.set_author(name="{}".format(
            ctx.message.author), icon_url=ctx.message.author.avatar_url)
        await msg.edit(embed=QuoteEmbed)

    @commands.command(name='company_profile', aliases=['comp_profile', 'cprofile', 'info'], help="Returns detailed information of Company")
    async def company_profile(self, ctx, cid=None):
        msg = await ctx.send(embed=Util.loading_embed)
        b = BSE()
        info = b.comp_profile(cid)
        try:
            if info['Name']:
                QuoteEmbed = discord.Embed(
                    title=f"{info['Name']}", description=f"{info['description']}\nSource: [bseindia.com](https://www.bseindia.com/)", colour=random.randint(0, 0xffffff))
                QuoteEmbed.add_field(
                    name="Website", value=f"{info['website']}", inline=False)
                QuoteEmbed.add_field(
                    name="Industry and Sector", value=f"{info['industry']}** ・ **{info['sector']}", inline=False)
        except:
            QuoteEmbed = discord.Embed(
                title="Sorry! No information available.", colour=random.randint(0, 0xffffff))
        QuoteEmbed.set_author(name="{}".format(
            ctx.message.author), icon_url=ctx.message.author.avatar_url)
        await msg.edit(embed=QuoteEmbed)

    @commands.command(name='analysis', aliases=['study', 'review', 'research'], help="Returns detailed analysis of Company")
    async def analysis(self, ctx, cid=None):
        msg = await ctx.send(embed=Util.loading_embed)
        b = BSE()
        info = b.analysis(cid)
        cs = b.quote(cid)
        QuoteEmbed = discord.Embed(
            title=f"{cs['stockName']}", description="Source: [bseindia.com](https://www.bseindia.com/)", colour=random.randint(0, 0xffffff))
        QuoteEmbed.add_field(name="Value Analysis", value=f"""
        :{info['value_analysis']['quality']['dot']}_circle: Quality - {info['value_analysis']['quality']['status']}
        :{info['value_analysis']['valuation']['dot']}_circle: Valuation - {info['value_analysis']['valuation']['status']}
        :{info['value_analysis']['technicals']['dot']}_circle: Technicals - {info['value_analysis']['technicals']['status']}
        :{info['value_analysis']['fintrend']['dot']}_circle: Fintrend - {info['value_analysis']['fintrend']['status']}
        """, inline=False)
        for daa in info['price_analysis']:
            if daa['dir'] == 0:
                daa['dir'] = 'Neutral'
            elif daa['dir'] == 1:
                daa['dir'] = 'Good'
            else:
                daa['dir'] = 'Bad'
            QuoteEmbed.add_field(
                name=f"{daa['header']} - {daa['dir']}", value=f"{daa['msg']}", inline=False)
        listToStr = '\n'.join(
            [str(elem) for elem in info['value_analysis']['technicaltext']])
        QuoteEmbed.add_field(name="Technical Text",
                             value=f"{listToStr}", inline=False)
        QuoteEmbed.set_author(name="{}".format(
            ctx.message.author), icon_url=ctx.message.author.avatar_url)
        await msg.edit(embed=QuoteEmbed)

def setup(client):
    client.add_cog(Stock(client))
