function remove_firm(a, apps)
    [filter(i -> i != a, worker) for worker in apps]
end

function applications(apps)
    apps = reverse(apps)
    picks = Array{Int64, 1}(length(apps))
    for i in 1:length(apps)
        a = apps[i]
        if length(a) > 0
            pick = maximum(a)
            apps = remove_firm(pick, apps)
            picks[i] = pick
        else
            picks[i] = -100
        end
    end
    reverse(picks)
end

workers = 1:1000
firms = 1:1000
apps = [sample(firms, 50, replace=false) for i in workers]
df = DataFrame(picks = applications(apps))
plot(df, y = "picks", Geom.point)


# show distribution of apps/firm
apps = [a for i in apps for a in i]
plot(x=counts(apps), Geom.histogram(bincount = 50))