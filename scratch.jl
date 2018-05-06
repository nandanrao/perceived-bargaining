workers = 1:1000
workers = reverse(workers)
firms = 1:1000

function remove_firm(a, apps)
    [filter(i -> i != a, worker) for worker in apps]
end


function applications(apps)
    picks = Array{Int64, 1}()
    for i in 1:length(apps)
        a = apps[i]
        if length(a) > 0
            pick = maximum(a)
            apps = remove_firm(pick, apps)
            append!(picks, pick)
        else
            append!(picks, -1)
        end
    end
    picks
end


apps = [sample(firms, 20, replace=false) for i in workers]
df = DataFrame(picks = reverse(applications(apps)))
plot(df, y = "picks", Geom.point)


# show distribution of apps/firm
apps = [a for i in apps for a in i]
plot(x=counts(apps), Geom.histogram(bincount = 50))
